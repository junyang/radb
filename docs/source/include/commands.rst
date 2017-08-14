Other Features
--------------

This section describes other useful RA features.

**Comments**:

  RA supports C/C++/Java-style comments.  ``//`` starts a single-line
  comment; text following ``//`` is considered comment and will be
  ignored.  ``/*`` and ``*/`` start and end (respectively) a possibly
  multi-line comment; text between them is considered comment and will
  be ignored.

**Command-line history editing**:

  On systems that support the `GNU Readline
  <https://en.wikipedia.org/wiki/GNU_Readline>`_, RA provides
  command-line input history and editing using arrow keys.  For
  example, Up/Down recall previous/next lines, and Left/Right move
  within the current line.

**Executing a script**: ``\source '``\ *ra_file*\ ``';``

  This command makes RA read statements from the specified file and
  execute them.  Note that *ra_file* must be enclosed in single
  quotes.  The file should be just a simple text file containing RA
  statements and comments.  This file can be prepared manually with a
  text editor, or it can be the result of a ``\save`` command.

**Executing SQL**: ``\sqlexec_{`` *sql_statement* ``};``

  With this command, you can send a SQL statement to the underlying
  database.  RA (and relational algebra) doesn't have its own language
  constructs for data definition (such as ``CREATE TABLE`` in SQL) or
  data modification (such as ``INSERT``, ``DELETE``, and ``UPDATE`` in
  SQL), this feature conveniently allows you to do all that without
  leaving RA.  Note that *sql_statement* should *NOT* be terminated by
  ``;`` (instead, ``;`` should terminate the RA command, following
  ``}``).  Some examples of using ``\sqlexec`` can be found in the
  ``.ra`` file for :codeurl:`creating the sample database
  </sample/beers.ra>`.
