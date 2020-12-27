Development guidelines
======================

Creating a dev environment
--------------------------

Create your personal fork of the project.
After cloning the environment ...

.. code :: shell

   $ git clone git@github.com:your username>/py-libhdate.git

If you don't have `poetry` installed on your system, take a look
at https://python-poetry.org/docs/#installation

Setup the virtual environment by installing the required packages:

.. code :: shell

   $ poetry install

At this point you should install the pre-commit hooks so your commits match those in
the project:

.. code :: shell

   $ poetry run pre-commit install

Create your topic branch

.. code :: shell

   $ git branch -b <topic>

Now you're ready to write you're code.
Once the code is ready ...

.. code :: shell

   $ poetry run tox

If tox passes, you're ready to create a pull request.

**Note:** the first commit might take some time while pre-commit installs the needed
dependencies.

**Important:** Your first commit message for a given branch will automatically be
added to the CHANGELOG. Please keep it clear. You can prepend the summary with ``chg``,
``fix`` or ``new`` to insert the message in the correct category.
Adding ``!minor`` or ``!cosmetics`` will cause the commit not to be noted in the
changelog.

Coding style guidelines
-----------------------

- We use black for all of our code formatting
- No large files are allowed.
- No commits to master are allowed.
