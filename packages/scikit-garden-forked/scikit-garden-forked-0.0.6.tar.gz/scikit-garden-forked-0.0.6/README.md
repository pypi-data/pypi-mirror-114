# Scikit-Garden

Forked from https://github.com/scikit-garden/scikit-garden


Scikit-Garden or skgarden (pronounced as skarden) is a garden for Scikit-Learn compatible decision trees and forests.



## Installation

Scikit-Garden depends on NumPy, SciPy, Scikit-Learn and Cython. So make sure these dependencies are installed using pip:

``
pip3 install setuptools numpy scipy scikit-learn cython
# or
pip3 install -r requirements.txt
``

After that my Scikit-Garden fork can be installed using pip.

``
pip install git+https://git@github.com/Demangio/scikit-garden.git
``

## Available models

### Regressors

* ExtraTreesRegressor (with `return_std` support)
* ExtraTreesQuantileRegressor
* RandomForestRegressor (with `return_std` support)
* RandomForestQuantileRegressor


## Usage

The estimators in Scikit-Garden are Scikit-Learn compatible and can serve as a drop-in replacement for Scikit-Learn's trees and forests.

``
from sklearn.datasets import load_boston
X, y = load_boston()


### Use QuantileForests for quantile estimation
from skgarden import RandomForestQuantileRegressor
rfqr = RandomForestQuantileRegressor(random_state=0)
rfqr.fit(X, y)
y_mean = rfqr.predict(X)
y_median = rfqr.predict(X, 50)
``

## What changes in this release

Change default predict method to the same as QuantReg package. This version is faster and include parametric estimation. 
Adaptation of code to higher versions of dependencies. 

## Important links
-  API Reference: https://scikit-garden.github.io/api/
-  Examples: https://scikit-garden.github.io/examples/
-  Modifications source: https://stackoverflow.com/questions/51483951/quantile-random-forests-from-scikit-garden-very-slow-at-making-predictions
