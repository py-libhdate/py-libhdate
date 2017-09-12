from setuptools import setup

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='hdate',
      version='0.5',
      description='Hebrew date and Zmanim',
      long_description=long_description,
      url='https://github.com/royi1000/py-libhdate',
      classifiers=[
           'Development Status :: 5 - Production/Stable',
           'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
           'Programming Language :: Python :: 2.7',
           'Programming Language :: Python :: 3'
      ],

      author='Royi Reshef',
      author_email='roy.myapp@gmail.com',
      maintainer='Tsvi Mostovicz',
      maintainer_email='ttmost@gmail.com',
      license='GPLv3+',
      packages=['hdate'],
      install_requires=[
          'python-dateutil'
      ],
      extras_require={'dev': ['tox']},
      python_requires='>=2.7'
      )
