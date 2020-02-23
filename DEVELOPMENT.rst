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
