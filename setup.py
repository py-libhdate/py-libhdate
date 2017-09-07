from setuptools import setup

setup(name='hdate',
      version='0.3',
      description='Hebrew date and Zmanim',
      url='https://github.com/royi1000/py-libhdate',
      classifiers=[
           'Development Status :: 5 - Production/Stable',
           'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
           'Programming Language :: Python :: 2.7'
      ],
      author='Royi Reshef',
      author_email='roy.myapp@gmail.com',
      maintainer='Tsvi Mostovicz',
      maintainer_email='ttmost@gmail.com',
      license='GPLv3+',
      packages=['hdate'],
      install_requires=[
        'python-dateutil',
        ],
      zip_safe=False)
