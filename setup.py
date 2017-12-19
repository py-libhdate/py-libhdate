#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from codecs import open
from glob import glob
from os.path import abspath
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup

here = abspath(dirname(__file__))

# Get the long description from the README file
with open(join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='hdate',
      version='0.6.1',
      description='Hebrew date and Zmanim',
      long_description=long_description,
      url='https://github.com/royi1000/py-libhdate',
      classifiers=[
           'Development Status :: 5 - Production/Stable',
           'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',  # noqa: E501
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3'
      ],

      author='Royi Reshef',
      author_email='roy.myapp@gmail.com',
      maintainer='Tsvi Mostovicz',
      maintainer_email='ttmost@gmail.com',
      license='GPLv3+',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
      install_requires=[
          'python-dateutil'
      ],
      extras_require={'dev': ['tox']},
      python_requires='>=2.7'
      )
