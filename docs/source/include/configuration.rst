Configuration File
------------------

RA relies on a :codeurl:`system configuration file </radb/sys.ini>`,
which you should not modify normally.  Then, RA looks for a user
configuration file named ``.radb.ini`` in your home directory (the
definition of "home directory" varies across operating systems).
Alternatively, you can specify a user configuration file using the
``-c`` option (see :ref:`Command-Line Options`).

The most important use of your user configuration file is to tell RA
how to connect to your own database server.  Some examples are given
in files with `.ini` suffix in the :codeurl:`sample directory
</sample>`, e.g., :codeurl:`postgresql.ini </sample/postgresql.ini>`.
You can copy one of these files to the default user configuration file
location and modify it to your liking.  See comments in these files
for instructions on how to set appropriate values for your database
system.

The user configuration file is divided into sections.  The first
section should be named ``[DEFAULT]``.  Subsequent sections can
provide additional customization that overrides the default.  For
example, with the sample :codeurl:`postgresql.ini
</sample/postgresql.ini>`, you will by default connect to PostgreSQL
server running locally on your computer, and you will need to give the
name of the database to connect to when you run RA (see
:ref:`Command-Line Options`).

.. note:: RA only installs the SQLite driver by default, so if you
   want to use it for other database systems, you will first need to
   install the appropriate drivers yourself.  For example, to install
   the PostgreSQL driver, simple use the command ``pip install
   psycopg2`` on your system (or ``pip3`` if Python 3 is not the
   default Python version on your system).

With the configuration file, you can do more.  Suppose you set
``db.database`` under ``[DEFAULT]``, and add two more sections as
follows::

  [DEFAULT]
  # ... other settings remain the same...
  db.database=beers
  # ... other settings remain the same...

  [play]
  db.database=pokemongo

  [production]
  db.username=me
  db.password=buzzword
  db.host=my.server.com
  db.port=5432
  db.database=mydb

Then, running RA without a *source* argument will connect you to the
``beers`` database on the local server by default; running RA with
``play`` as the *source* argument will connect you to the local
``pokemongo`` database (in this case, using ``pokemongo`` as *source*
would achieve the same effect); finally, running RA with
``production`` as *source* will connect you to the ``mydb`` database
running on the remote server, using the credentials supplied under the
``[production]`` section.

Another use of the configuration file to declare to RA useful built-in
functions support by your database system.  This use is discussed
further below.

Specification of Built-in Functions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Specifying a built-in function in the configuration file makes RA
aware of its signature and allows RA to check its input and out output
types (see also :ref:`Type Checking`), which helps catch errors in
queries.  In fact, RA specifies all operators and functions that are
known to work across database vendors in its :codeurl:`system
configuration file </radb/sys.ini>` under the setting for
``default_functions``.  Additionally, RA looks for a setting for
``functions`` in the user configuration file, which can supplement or
override specifications in ``default_functions``.

In both settings, each function is declared with a single line of
text, with the following format:

*fname* ``(``\ *req_t1*\ ``,`` *req_t2*\ ``,`` ... ``,`` *opt_t1*\
``?,`` *opt_t2*\ ``?,`` ... ``,`` *opt_tlast*\ ``*) ->`` *return_t*

Here, *fname* is the name of the function; upper-case function names
in the :codeurl:`system configuration file </radb/sys.ini>` are
reserved for special operators.  The (possibly empty) sequence
*req_t1*, *req_t2*, ... specifies the types of required arguments.
The (possibly empty) sequence *opt_t1*, *opt_t2*, ..., each suffixed
by ``?``, specifies the types of optional arguments.  The optional
*opt_tlast* suffixed by ``*`` specifies that the function can take an
arbitrary number of additional arguments of the given type at the end.
Finally, *return_t* specifies the result type of the function.  These
types can be any of the basic value types supported by RA, as well as
``any`` (see :ref:`Data Types and Operators`).

You can also specify a function as an aggregate, by prefixing the
declaration line with keyword ``aggregate:`` (before *fname*).  An
aggregate function takes a (multi)set of input tuples, each with
attribute(s) matching the declared argument specification, and
computes a single output value of the declared return type.  These
functions can be used in the aggregation operator ``\aggr`` (see
:ref:`Basic Usage`).

Comments can be added with ``#``; text following ``#`` will be
ignored.  There cannot be empty lines between function declarations.
The order of declarations is important; see :ref:`Type Checking` for
details.

.. warning:: Recall from discussion in :ref:`Type Checking` that in
   general, a function can have multiple signatures.  Suppose your
   user configuration file gives (at least) one declaration for an
   operator/function *f* already declared in the :codeurl:`system
   configuration file </radb/sys.ini>`.  In this case, RA assumes that
   you intend to wipe out all system default declarations for *f*, and
   would like to use only your own declarations for *f*.  (This
   behavior is necessitated by RA's simple, order-based resolution
   discussed in :ref:`Type Checking`, because we need a way for user
   configuration to customize the order of declarations.)  An
   implication of this rule is that you must remember to declare all
   alternative signatures for *f* in your user configuration file.
