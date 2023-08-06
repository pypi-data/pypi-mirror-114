#! /usr/bin/env python

from distutils.version import LooseVersion
import os

import numpy as np
from setuptools import Extension, find_packages, setup


DISTNAME = 'scikit-garden-forked'
DESCRIPTION = "A garden of scikit-learn compatible trees"
URL = 'https://github.com/Demangio/scikit-garden'
MAINTAINER = 'Guillaume'
MAINTAINER_EMAIL = 'guillaumedemange@free.fr'
LICENSE = 'new BSD'
VERSION = '0.0.1'

CYTHON_MIN_VERSION = '0.23'


message = ('Please install cython with a version >= {0} in order '
           'to build a scikit-garden development version.').format(
           CYTHON_MIN_VERSION)
try:
    import Cython
    if LooseVersion(Cython.__version__) < CYTHON_MIN_VERSION:
        message += ' Your version of Cython was {0}.'.format(
            Cython.__version__)
        raise ValueError(message)
    from Cython.Build import cythonize
except ImportError as exc:
    exc.args += (message,)
    raise

libraries = []
if os.name == 'posix':
    libraries.append('m')


if __name__ == "__main__":
    setup(name=DISTNAME,
          maintainer=MAINTAINER,
          maintainer_email=MAINTAINER_EMAIL,
          packages=find_packages(),
          include_package_data=True,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          version=VERSION,
          zip_safe=False,  # the package can run out of an .egg file
          classifiers=[
              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',
              'License :: OSI Approved',
              'Programming Language :: C',
              'Programming Language :: Python',
              'Topic :: Software Development',
              'Topic :: Scientific/Engineering',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Operating System :: Unix',
              'Operating System :: MacOS'
            ],
          install_requires=["numpy", "scipy", "scikit-learn>=0.18", "cython"],
          setup_requires=["cython"]
         )
