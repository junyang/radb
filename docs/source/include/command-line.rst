Command-Line Options
--------------------

RA provides a number of command-line options.  To see a complete list,
run RA with command-line flag ``-h`` (for help).  Some of the most
useful ones are listed below.

* Use ``-c`` (``--configfile``) *config_file* to specify a RA user
  configuration file.  Among other things, the user configuration file
  is useful for telling RA how to connect to your own database server.
  See :ref:`Configuration File` for more details.

* Use ``-v`` (``--verbose``) to have RA show more information.  This
  flag is useful for debugging, as RA will show you a tree
  representation of the RA query you entered.  Use ``-d`` (``--debug``)
  if you want to see even more information, e.g., the SQL translation
  of your RA query.

* Use ``-i`` (``--inputfile``) *input_file* to specify a file of
  statements for RA to run.  In this case, RA runs in non-interactive
  mode (you won't get the RA prompt), and simply print out the output
  from executing the statements.  Here, to get a more complete record
  of the execution, you can additionally use ``-e`` (``--echo``) to
  tell RA to echo all statements it reads to the output as well.

* Use ``-o`` (``--outputfile``) *output_file* to specify a file to
  which RA will write its output (in addition to printing that out).
  Together with ``-e``, ``-o`` will give you a complete record of your
  RA session, which is especially useful for recording what you did in
  an interactive session.

* The optional *source* argument (without a flag) specifies the data
  source you want to connect to.  It can be the name of a section in
  your user configuration file (under which RA can find detailed
  connection information), or the name of the database you are
  connecting to (assuming default for other connection information).
  See :ref:`Configuration File` for details.
