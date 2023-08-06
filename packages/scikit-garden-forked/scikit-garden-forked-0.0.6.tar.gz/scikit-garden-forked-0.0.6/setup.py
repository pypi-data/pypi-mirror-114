#! /usr/bin/env python

from distutils.version import LooseVersion
import os

from setuptools import Extension, find_packages, setup


DISTNAME = 'scikit-garden-forked'
DESCRIPTION = "A garden of scikit-learn compatible trees, and I had few modifications to it."
URL = 'https://github.com/Demangio/scikit-garden'
MAINTAINER = 'Guillaume'
MAINTAINER_EMAIL = 'guillaumedemange@free.fr'
LICENSE = 'new BSD'
VERSION = '0.0.6'

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

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
          long_description=long_description,
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
          install_requires=requirements,
         )
