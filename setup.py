from setuptools import setup

setup(name='hdate',
      version='0.1',
      description='Hebrew date and Zmanim',
      url='https://github.com/royi1000/py-libhdate',
      author='Royi Reshef',
      author_email='roy.myapp@gmail.com',
      license='MIT',
      packages=['hdate'],
      install_requires=[
        'python-dateutil',
        ],
      zip_safe=False)
