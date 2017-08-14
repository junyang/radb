Getting Started
===============

* Make sure you have **Python 3.5 or higher** on your system (you can
  check using ``python --version``).  Then install RA using ``pip``::

    pip install radb

  .. note:: We recommend you install the `Anaconda distribution
     <https://www.continuum.io/downloads>`_ of Python; be sure to
     download the latest Python 3 version.

  .. note:: If Python 3 is not the default Python version on your
     system, you may need to run ``pip3`` instead of ``pip``.

* To set up a sample SQLite database to use RA with:

  - Download :rawcodeurl:`beers.ra </sample/beers.ra>`, the RA script
    for creating the sample database.

  - Issue the following command, which will create a SQLite database
    file named ``beers.db`` in the same directory::

      radb -i beers.ra beers.db

  .. attention:: If your system complains about not being able to find
     the command ``radb``, the command was probably installed
     somewhere that's not on your command path.  On Linux, for
     example, it may be located in ``~/.local/bin/``.  You can always
     include the path when running RA (e.g., ``~/.local/bin/radb``),
     or add the path to your command path so you don't need to type it
     every time.  To find out where exactly ``pip`` installed ``radb``
     on your system, examine the output of the following command::

       pip show -f radb

  - Then you can run RA on the sample database::

      radb beers.db

  - At RA's ``ra>`` prompt, you can list the relations in the sample
    database, try some relational algebra queries, and quit::

      \list;
      \select_{name like 'B%'} Beer;
      \quit;

* If you want to use RA with a different database system, or to set it
  up such that you don't need to type a long list of command-line
  arguments every time you run RA, see :ref:`Configuration File`.
