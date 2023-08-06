from __future__ import division
import numpy as np
from numpy import ma
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
try:
    from sklearn.ensemble.forest import ForestRegressor
    from sklearn.ensemble.base import BaseEnsemble
except:
    # for higher versions
    from sklearn.ensemble._forest import ForestRegressor
    from sklearn.ensemble._base import BaseEnsemble

from sklearn.utils import check_array
from sklearn.utils import check_random_state
from sklearn.utils import check_X_y

from .tree import DecisionTreeQuantileRegressor
from .tree import ExtraTreeQuantileRegressor
from .utils import weighted_percentile

import scipy.stats as scp
from scipy.optimize import fsolve

import warnings


def generate_sample_indices(random_state, n_samples):
    """
    Generates bootstrap indices for each tree fit.

    Parameters
    ----------
    random_state: int, RandomState instance or None
        If int, random_state is the seed used by the random number generator.
        If RandomState instance, random_state is the random number generator.
        If None, the random number generator is the RandomState instance used
        by np.random.

    n_samples: int
        Number of samples to generate from each tree.

    Returns
    -------
    sample_indices: array-like, shape=(n_samples), dtype=np.int32
        Sample indices.
    """
    random_instance = check_random_state(random_state)
    sample_indices = random_instance.randint(0, n_samples, n_samples)
    return sample_indices


class BaseForestQuantileRegressor(ForestRegressor):
    def fit(self, X, y):
        """
        Build a forest from the training set (X, y).

        Parameters
        ----------
        X : array-like or sparse matrix, shape = [n_samples, n_features]
            The training input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csc_matrix``.

        y : array-like, shape = [n_samples] or [n_samples, n_outputs]
            The target values (class labels) as integers or strings.

        sample_weight : array-like, shape = [n_samples] or None
            Sample weights. If None, then samples are equally weighted. Splits
            that would create child nodes with net zero or negative weight are
            ignored while searching for a split in each node. Splits are also
            ignored if they would result in any single class carrying a
            negative weight in either child node.

        check_input : boolean, (default=True)
            Allow to bypass several input checking.
            Don't use this parameter unless you know what you do.

        X_idx_sorted : array-like, shape = [n_samples, n_features], optional
            The indexes of the sorted training input samples. If many tree
            are grown on the same dataset, this allows the ordering to be
            cached between trees. If None, the data will be sorted here.
            Don't use this parameter unless you know what to do.

        Returns
        -------
        self : object
            Returns self.
        """
        # apply method requires X to be of dtype np.float32
        X, y = check_X_y(
            X, y, accept_sparse="csc", dtype=np.float32, multi_output=False)
        super(BaseForestQuantileRegressor, self).fit(X, y)

        self.y_train_ = y
        self.y_train_leaves_ = -np.ones((self.n_estimators, len(y)), dtype=np.int32)
        self.y_weights_ = np.zeros_like((self.y_train_leaves_), dtype=np.float32)

        for i, est in enumerate(self.estimators_):
            if self.bootstrap:
                bootstrap_indices = generate_sample_indices(
                    est.random_state, len(y))
            else:
                bootstrap_indices = np.arange(len(y))

            est_weights = np.bincount(bootstrap_indices, minlength=len(y))
            y_train_leaves = est.y_train_leaves_
            for curr_leaf in np.unique(y_train_leaves):
                y_ind = y_train_leaves == curr_leaf
                self.y_weights_[i, y_ind] = (
                    est_weights[y_ind] / np.sum(est_weights[y_ind]))

            self.y_train_leaves_[i, bootstrap_indices] = y_train_leaves[bootstrap_indices]
        return self

    
#########################################################################################################################
############# original skgarden predict method which is very slow #######################################################
#########################################################################################################################
    def original_predict(self, X, quantile=None):
        """
        Predict regression value for X.

        Parameters
        ----------
        X : array-like or sparse matrix of shape = [n_samples, n_features]
            The input samples. Internally, it will be converted to
            ``dtype=np.float32`` and if a sparse matrix is provided
            to a sparse ``csr_matrix``.

        quantile : int, optional
            Value ranging from 0 to 100. By default, the mean is returned.

        check_input : boolean, (default=True)
            Allow to bypass several input checking.
            Don't use this parameter unless you know what you do.

        Returns
        -------
        y : array of shape = [n_samples]
            If quantile is set to None, then return E(Y | X). Else return
            y such that F(Y=y | x) = quantile.
        """
        # apply method requires X to be of dtype np.float32
        X = check_array(X, dtype=np.float32, accept_sparse="csc")
        if quantile is None:
            return super(BaseForestQuantileRegressor, self).predict(X)

        sorter = np.argsort(self.y_train_)
        X_leaves = self.apply(X)
        weights = np.zeros((X.shape[0], len(self.y_train_)))
        quantiles = np.zeros((X.shape[0]))
        for i, x_leaf in enumerate(X_leaves):
            mask = self.y_train_leaves_ != np.expand_dims(x_leaf, 1)
            x_weights = ma.masked_array(self.y_weights_, mask)
            weights = x_weights.sum(axis=0)
            quantiles[i] = weighted_percentile(
                self.y_train_, quantile, weights, sorter)
        return quantiles

#########################################################################################################################
#########################################################################################################################
# adapted from
# https://stackoverflow.com/questions/51483951/quantile-random-forests-from-scikit-garden-very-slow-at-making-predictions
#########################################################################################################################
#########################################################################################################################
    def predict(self, X_test, quantiles=None, moments=-1, verbose=False, seed=None):
        """
        Function to predict quantiles much faster than the default skgarden method
        This is the same method that the ranger and quantRegForest packages in R use
        Output is (n_samples, n_quantiles) or (n_samples, ) if a scalar is given as quantiles
        """
        if seed is not None:
            np.random.seed(seed)
        
        # if nothing is specified, returns same as sklearn RandomForestRegressor
        if (quantiles is None) & (moments==0):
            if verbose:
                print("Returns RandomForestRegressor result")
            return super(BaseForestQuantileRegressor, self).predict(X_test)
        
        # Begin one-time calculation of random_values. This only depends on model, so could be saved.
        n_leaves = np.max(self.y_train_leaves_) + 1  # leaves run from 0 to max(leaf_number)
        random_values = np.zeros((self.n_estimators, n_leaves))
        for tree in range(self.n_estimators):
            for leaf in range(n_leaves):
                train_samples = np.argwhere(self.y_train_leaves_[tree, :] == leaf).reshape(-1)
                if len(train_samples) == 0:
                    random_values[tree, leaf] = np.nan
                else:
                    train_values = self.y_train_[train_samples]
                    random_values[tree, leaf] = np.random.choice(train_values)
        # Optionally, save random_values as a model attribute for reuse later

        # For each sample, get the random leaf values from all the leaves they land in
        X_leaves = self.apply(X_test)
        leaf_values = np.zeros((X_test.shape[0], self.n_estimators))
        for i in range(self.n_estimators):
            leaf_values[:, i] = random_values[i, X_leaves[:, i]]
        
        # RandomForest has the full distribution in memory. You can return moments, quantiles, or everything else
        mean = np.mean(leaf_values, axis=1)
        std = np.std(leaf_values, axis=1)
        skew = scp.skew(leaf_values, axis=1)
        kurt = scp.kurtosis(leaf_values, axis=1)
        
        # returns param "moments" first moments
        if (moments == 1) & (quantiles is None):
            # returns mean, exactly the same as RandomForestRegressor
            if verbose:
                print("Returns mean")
            return mean.reshape(-1,1)
        
        elif (moments == 2) & (quantiles is None):
            # returns mean and std
            if verbose:
                print("Returns mean, std")
            return np.concatenate((mean.reshape(-1,1), std.reshape(-1,1)), axis = 1)
        
        elif (moments == 3) & (quantiles is None):
            # returns mean, std, skewness
            if verbose:
                print("Returns mean, std, skewness")
            return np.concatenate((mean.reshape(-1,1), std.reshape(-1,1), skew.reshape(-1,1)), axis = 1)

        elif (moments == 4) & (quantiles is None):
            # returns mean, std, skewness, kurtosis
            if verbose:
                print("Returns mean, std, skewness, kurtosis")
            return np.concatenate((mean.reshape(-1,1), std.reshape(-1,1), skew.reshape(-1,1), kurt.reshape(-1,1)), axis = 1)
        
        # return quantiles given probability distribution
        # deterministic
        elif (quantiles is not None) & (moments==1):
            if verbose:
                print("Deterministic quantiles")
            return np.array([mean for i in quantiles]).transpose()
        # normal fit
        elif (quantiles is not None) & (moments==2):
            return scp.norm.ppf(quantiles, loc=mean.reshape(-1,1), scale=std.reshape(-1,1))
        
        
#######################################################################################
############# A BIT MORE COMPLEX (AND SLOWER): INTEGRATE SKEWNESS IN MOMENTS ##########
        elif (quantiles is not None) & (moments==3):
        
            if verbose:
                print("Skew normal quantiles")
        
            def mean_skewnormal(loc, scale, shape):
                delta = shape/np.sqrt(1+shape**2)
                return loc + scale*delta*np.sqrt(2/np.pi)

            def skewness_skewnormal(shape):
                delta = shape/np.sqrt(1+shape**2)
                return (4-np.pi)/2 * (delta*np.sqrt(2/np.pi))**3 / (1 - 2*delta**2/np.pi)**(3/2)

            def std_skewnormal(scale, shape):
                delta = shape/np.sqrt(1+shape**2)
                return scale * np.sqrt(1 - 2*delta**2/np.pi)

            # from skewnormal parameters (loc, scale, a) to moments (mean, std, skewness)
            def moments(params):
                return np.array([mean_skewnormal(params[0], params[1], params[2]),
                                 std_skewnormal(params[1], params[2]),
                                 skewness_skewnormal(params[2])])

            # moments inverse fonction: from (mean, std, skewness) to (loc, scale, a)
            def params(mean, std, skew):
                parameters = np.zeros((len(mean), 3))
                warnings.filterwarnings("error", category=RuntimeWarning)
                for i in range(len(mean)):
                    skew[i] = min(.99, max(skew[i], -.99))
                    fct = lambda x: moments(x) - np.array([mean[i], std[i], skew[i]])
                    ok = False
                    while not ok:
                        try:
                            parameters[i] = fsolve(fct, [np.random.uniform(-1,1), np.random.uniform(0,1), np.random.uniform(-1,1)])
                            ok = True
                        except:
                            ok = False
                    if verbose:
                        print(f"found {i+1}/{len(mean)} skewnormal parameters", end="\r")
                
                warnings.resetwarnings()
                return parameters.T
            
            loc, scale, a = params(mean, std, skew)
            if verbose:
                print("parameters determined for each sample        ")
                print("construct quantiles with skewnormal percent point function,")
                print(f"note that function scipy.stats.skewnorm.ppf takes roughly 10ms per sample per quantile, it may take {round(len(quantiles)*len(X_test)*0.01)}s")
            return scp.skewnorm.ppf(quantiles, loc=loc.reshape(-1,1), scale=scale.reshape(-1,1), a=a.reshape(-1,1))
#######################################################################################



        # Non parametric: for each sample, calculate the quantiles of the leaf_values
        elif (quantiles is not None) & ((moments<0) | (moments>3)):
            if verbose:
                print("Non parametric quantiles")
            return np.quantile(leaf_values, np.array(quantiles), axis=1).transpose()
        
        else:
            warnings.warn("Incorrect parameters, returns None")
            return None

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################

class RandomForestQuantileRegressor(BaseForestQuantileRegressor):
    """
    A random forest regressor that provides quantile estimates.

    A random forest is a meta estimator that fits a number of classifying
    decision trees on various sub-samples of the dataset and use averaging
    to improve the predictive accuracy and control over-fitting.
    The sub-sample size is always the same as the original
    input sample size but the samples are drawn with replacement if
    `bootstrap=True` (default).

    Parameters
    ----------
    n_estimators : integer, optional (default=10)
        The number of trees in the forest.

    criterion : string, optional (default="mse")
        The function to measure the quality of a split. Supported criteria
        are "mse" for the mean squared error, which is equal to variance
        reduction as feature selection criterion, and "mae" for the mean
        absolute error.
        .. versionadded:: 0.18
           Mean Absolute Error (MAE) criterion.

    max_features : int, float, string or None, optional (default="auto")
        The number of features to consider when looking for the best split:
        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a percentage and
          `int(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=n_features`.
        - If "sqrt", then `max_features=sqrt(n_features)`.
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.
        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    max_depth : integer or None, optional (default=None)
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.

    min_samples_split : int, float, optional (default=2)
        The minimum number of samples required to split an internal node:
        - If int, then consider `min_samples_split` as the minimum number.
        - If float, then `min_samples_split` is a percentage and
          `ceil(min_samples_split * n_samples)` are the minimum
          number of samples for each split.
        .. versionchanged:: 0.18
           Added float values for percentages.

    min_samples_leaf : int, float, optional (default=1)
        The minimum number of samples required to be at a leaf node:
        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a percentage and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.
        .. versionchanged:: 0.18
           Added float values for percentages.

    min_weight_fraction_leaf : float, optional (default=0.)
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.

    max_leaf_nodes : int or None, optional (default=None)
        Grow trees with ``max_leaf_nodes`` in best-first fashion.
        Best nodes are defined as relative reduction in impurity.
        If None then unlimited number of leaf nodes.

    bootstrap : boolean, optional (default=True)
        Whether bootstrap samples are used when building trees.

    oob_score : bool, optional (default=False)
        whether to use out-of-bag samples to estimate
        the R^2 on unseen data.

    n_jobs : integer, optional (default=1)
        The number of jobs to run in parallel for both `fit` and `predict`.
        If -1, then the number of jobs is set to the number of cores.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    verbose : int, optional (default=0)
        Controls the verbosity of the tree building process.

    warm_start : bool, optional (default=False)
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just fit a whole
        new forest.

    Attributes
    ----------
    estimators_ : list of DecisionTreeQuantileRegressor
        The collection of fitted sub-estimators.

    feature_importances_ : array of shape = [n_features]
        The feature importances (the higher, the more important the feature).

    n_features_ : int
        The number of features when ``fit`` is performed.

    n_outputs_ : int
        The number of outputs when ``fit`` is performed.

    oob_score_ : float
        Score of the training dataset obtained using an out-of-bag estimate.

    oob_prediction_ : array of shape = [n_samples]
        Prediction computed with out-of-bag estimate on the training set.

    y_train_ : array-like, shape=(n_samples,)
        Cache the target values at fit time.

    y_weights_ : array-like, shape=(n_estimators, n_samples)
        y_weights_[i, j] is the weight given to sample ``j` while
        estimator ``i`` is fit. If bootstrap is set to True, this
        reduces to a 2-D array of ones.

    y_train_leaves_ : array-like, shape=(n_estimators, n_samples)
        y_train_leaves_[i, j] provides the leaf node that y_train_[i]
        ends up when estimator j is fit. If y_train_[i] is given
        a weight of zero when estimator j is fit, then the value is -1.

    References
    ----------
    .. [1] Nicolai Meinshausen, Quantile Regression Forests
        http://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf
    """
    def __init__(self,
                 n_estimators=10,
                 criterion='mse',
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.0,
                 max_features='auto',
                 max_leaf_nodes=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=1,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        super(RandomForestQuantileRegressor, self).__init__(
            base_estimator=DecisionTreeQuantileRegressor(),
            n_estimators=n_estimators,
            estimator_params=("criterion", "max_depth", "min_samples_split",
                              "min_samples_leaf", "min_weight_fraction_leaf",
                              "max_features", "max_leaf_nodes",
                              "random_state"),
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start)

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes


class ExtraTreesQuantileRegressor(BaseForestQuantileRegressor):
    """
    An extra-trees regressor that provides quantile estimates.

    This class implements a meta estimator that fits a number of
    randomized decision trees (a.k.a. extra-trees) on various sub-samples
    of the dataset and use averaging to improve the predictive accuracy
    and control over-fitting.

    Parameters
    ----------
    n_estimators : integer, optional (default=10)
        The number of trees in the forest.

    criterion : string, optional (default="mse")
        The function to measure the quality of a split. Supported criteria
        are "mse" for the mean squared error, which is equal to variance
        reduction as feature selection criterion, and "mae" for the mean
        absolute error.
        .. versionadded:: 0.18
           Mean Absolute Error (MAE) criterion.

    max_features : int, float, string or None, optional (default="auto")
        The number of features to consider when looking for the best split:
        - If int, then consider `max_features` features at each split.
        - If float, then `max_features` is a percentage and
          `int(max_features * n_features)` features are considered at each
          split.
        - If "auto", then `max_features=n_features`.
        - If "sqrt", then `max_features=sqrt(n_features)`.
        - If "log2", then `max_features=log2(n_features)`.
        - If None, then `max_features=n_features`.
        Note: the search for a split does not stop until at least one
        valid partition of the node samples is found, even if it requires to
        effectively inspect more than ``max_features`` features.

    max_depth : integer or None, optional (default=None)
        The maximum depth of the tree. If None, then nodes are expanded until
        all leaves are pure or until all leaves contain less than
        min_samples_split samples.

    min_samples_split : int, float, optional (default=2)
        The minimum number of samples required to split an internal node:
        - If int, then consider `min_samples_split` as the minimum number.
        - If float, then `min_samples_split` is a percentage and
          `ceil(min_samples_split * n_samples)` are the minimum
          number of samples for each split.
        .. versionchanged:: 0.18
           Added float values for percentages.

    min_samples_leaf : int, float, optional (default=1)
        The minimum number of samples required to be at a leaf node:
        - If int, then consider `min_samples_leaf` as the minimum number.
        - If float, then `min_samples_leaf` is a percentage and
          `ceil(min_samples_leaf * n_samples)` are the minimum
          number of samples for each node.
        .. versionchanged:: 0.18
           Added float values for percentages.

    min_weight_fraction_leaf : float, optional (default=0.)
        The minimum weighted fraction of the sum total of weights (of all
        the input samples) required to be at a leaf node. Samples have
        equal weight when sample_weight is not provided.

    max_leaf_nodes : int or None, optional (default=None)
        Grow trees with ``max_leaf_nodes`` in best-first fashion.
        Best nodes are defined as relative reduction in impurity.
        If None then unlimited number of leaf nodes.

    bootstrap : boolean, optional (default=False)
        Whether bootstrap samples are used when building trees.

    oob_score : bool, optional (default=False)
        Whether to use out-of-bag samples to estimate the R^2 on unseen data.

    n_jobs : integer, optional (default=1)
        The number of jobs to run in parallel for both `fit` and `predict`.
        If -1, then the number of jobs is set to the number of cores.

    random_state : int, RandomState instance or None, optional (default=None)
        If int, random_state is the seed used by the random number generator;
        If RandomState instance, random_state is the random number generator;
        If None, the random number generator is the RandomState instance used
        by `np.random`.

    verbose : int, optional (default=0)
        Controls the verbosity of the tree building process.

    warm_start : bool, optional (default=False)
        When set to ``True``, reuse the solution of the previous call to fit
        and add more estimators to the ensemble, otherwise, just fit a whole
        new forest.

    Attributes
    ----------
    estimators_ : list of ExtraTreeQuantileRegressor
        The collection of fitted sub-estimators.

    feature_importances_ : array of shape = [n_features]
        The feature importances (the higher, the more important the feature).

    n_features_ : int
        The number of features when ``fit`` is performed.

    n_outputs_ : int
        The number of outputs when ``fit`` is performed.

    oob_score_ : float
        Score of the training dataset obtained using an out-of-bag estimate.

    oob_prediction_ : array of shape = [n_samples]
        Prediction computed with out-of-bag estimate on the training set.

    y_train_ : array-like, shape=(n_samples,)
        Cache the target values at fit time.

    y_weights_ : array-like, shape=(n_estimators, n_samples)
        y_weights_[i, j] is the weight given to sample ``j` while
        estimator ``i`` is fit. If bootstrap is set to True, this
        reduces to a 2-D array of ones.

    y_train_leaves_ : array-like, shape=(n_estimators, n_samples)
        y_train_leaves_[i, j] provides the leaf node that y_train_[i]
        ends up when estimator j is fit. If y_train_[i] is given
        a weight of zero when estimator j is fit, then the value is -1.

    References
    ----------
    .. [1] Nicolai Meinshausen, Quantile Regression Forests
        http://www.jmlr.org/papers/volume7/meinshausen06a/meinshausen06a.pdf
    """
    def __init__(self,
                 n_estimators=10,
                 criterion='mse',
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.0,
                 max_features='auto',
                 max_leaf_nodes=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=1,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        super(ExtraTreesQuantileRegressor, self).__init__(
            base_estimator=ExtraTreeQuantileRegressor(),
            n_estimators=n_estimators,
            estimator_params=("criterion", "max_depth", "min_samples_split",
                              "min_samples_leaf", "min_weight_fraction_leaf",
                              "max_features", "max_leaf_nodes",
                              "random_state"),
            bootstrap=bootstrap,
            oob_score=oob_score,
            n_jobs=n_jobs,
            random_state=random_state,
            verbose=verbose,
            warm_start=warm_start)

        self.criterion = criterion
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf
        self.min_weight_fraction_leaf = min_weight_fraction_leaf
        self.max_features = max_features
        self.max_leaf_nodes = max_leaf_nodes
