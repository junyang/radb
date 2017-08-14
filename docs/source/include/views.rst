Views
-----

RA lets you define "views," which may be thought of as temporary,
relation-valued variables holding the results of relational algebra
expressions.  To define a view, use the syntax:

*view_name* ``:-`` *view_definition_query*\ ``;``

Once you define a view, it will show up in ``\list``, and you can use
it later in queries (including queries that define other views) as if
it's a database relation.  Whenever RA evaluates a query, it basically
"expands" any view reference in the query by replacing the view
reference with the corresponding view definition query.  If that
definition query itself contains other view references, RA will expand
them recursively.  In the end, RA always evaluate a query starting
from database relations.  The output relation schema from a view
reference is the output relation schema for the corresponding view
definition query, but with all relation names in all attribute
specifications set to the view name.

To undefine a view (i.e., to forget its definition), use the command
``\clear`` *view_name*\ ``;``.  RA won't let you undefine a view if it
is used to define other views.  However, you can add ``!`` after
``\clear`` to undefine *view_name* as well as every view dependent on
it (directly or indirectly) "by force."  You can also use ``\clear *``
to undefine all views.

RA allows you to redefine a view.  It will even let you redefine a
view *v* when there are other views defined using *v*, provided that
all (directly or indirectly) dependent view definitions still make
sense with the redefined *v*, and that this redefinition doesn't lead
to any circular definition.

Finally, you can save view definitions to files and load them back
into an RA session.  The command ``\save`` *view_name* ``'``\
*file_name*\ ``';`` saves the definition of the given view as well as
those of all prerequisite views in the specified file; note that
*file_name* need be surrounded in single quotes.  If you do not
specify the file name, the default file name will be *view_name*\
``.ra``.  You can also use ``*`` in place of *view_name*; in this case
RA will save all your views in a file whose name defaults to
``views.ra``.  RA will not let you overwrite an existing file, unless
you add ``!`` after ``\save``.

.. warning:: Once you exit from RA, you lose all views you have
   defined in the session.  So make sure you save what you want before
   exiting!
