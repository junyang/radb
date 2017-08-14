Cheat Sheet
===========

THIS SECTION IS UNDER DEVELOPMENT.

.. list-table::
   :header-rows: 0

   * - ``\quit;``
     - Exit from RA
   * - ``\list;``
     - List database tables and user-defined views
   * - ``\clear *;``
     - Clear all user view definitions
   * - ``\clear!``\  *v*\ ``;``
     - Clear definition for view *v* as well as any views that depend
       on *v* (directly or indirectly)
   * - ``\save '``\ *file.ra*\ ``';``
     - Save all user view definitions to *file.ra*
   * - ``\save``\  *v*\  ``'``\ *file.ra*\ ``';``
     - Save to *file.ra* the definition of view *v* as well as
       definitions of any views that *v* depends on (directly or
       indirectly)
   * - ``\source '``\ *ra_file*\ ``';``
     - Execute RA statements from *ra_file*
   * - ``\sqlexec_{`` *sql_statement* ``};``
     - Execute the SQL statement (a single one, not terminated by
       ``;`` itself) in the underlying database
