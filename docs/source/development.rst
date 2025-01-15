Development guidelines
======================

Creating a dev environment
--------------------------

If you don't have `pdm` installed on your system, take a look
at ``https://pdm-project.org/latest/#installation``

Setup the virtual environment by installing the required packages:

.. code:: shell

   $ pdm install

At this point you should install the pre-commit hooks so your commits match those in
the project:

.. code:: shell

   $ pdm run pre-commit install

Create your topic branch

.. code:: shell

   $ git branch -b <topic>

Now you're ready to write you're code.
Once the code is ready ...

.. code:: shell

   $ pdm run tox

If tox passes, you're ready to create a pull request.

**Note:** the first commit might take some time while pre-commit installs the needed
dependencies.

Using a different Python version
--------------------------------

PDM allows you natively to install and use a different Python version during your development.

.. code:: shell

   $ pdm python install 3.12  # Or any version from 3.8 onwards
   $ pdm use                  # Will provide you a list of installed Pythons, including the one you installed
   $ pdm install              # Recreate your virtual environment


Coding style guidelines
-----------------------

- We use black for all of our code formatting
- No large files are allowed.
- No commits to master are allowed.
