Dev notes
=========

To create a dev environment, run the following commands:

.. code :: shell

   $ python3 -m venv hdate
   $ cd hdate
   $ . bin/activate
   $ git clone git@github.com:royi1000/py-libhdate.git
   $ python setup.py develop
   $ pip install .[dev]

Now you're ready to write you're code.
Once the code is ready ...

.. code :: shell

   $ tox

If tox passes, you're ready to create a pull request.

Publishing code
***************
Once code maintainers have accepted the code they should run the following tools:

1. ``pip install .[pub]`` to install the tools necessary for publishing the package.
2. ``bumpversion`` to update the version using arguments ``major``, ``minor`` or ``patch`` depending on the changes.
3. ``python setup.py bdist_wheel`` to generate a binary distribution.
4. ``twine upload dist/*`` to upload the binaries to pypi.
