Cheat Sheet
===========

Relational Operators
--------------------

.. list-table::
   :header-rows: 0

   * - **Selection**
   * - ``\select_{``\ *condition*\ ``}`` *input_relation*
         output the tuples in *input_relation* that satisfy *condition*

   * - **Projection**
   * - ``\project_{``\ *attr_list*\ ``}`` *input_relation*
         output only the attributes in *attr_list* for each tuple in
         *input_relation* (duplicate output tuples are removed)

   * - **Theta-Join**
   * - *input_relation_1* ``\join_{``\ *cond*\ ``}`` *input_relation_2*
         find pairs of tuples from *input_relation_1* and
         *input_relation_2* that satisfy *cond*, and for each such
         pair output the concatenation of the two tuples

   * - **Natural join**
   * - *input_relation_1* ``\join`` *input_relation_2*
         find pairs of tuples from *input_relation_1* and
         *input_relation_2* that agree on the values of all commonly
         named attributes, and for each pair output the concatenation
         of the two tuples (with only one copy of the commonly named
         attributes)

   * - **Cross product**
   * - *input_relation_1* ``\cross`` *input_relation_2*
         enumerate all pairs of tuples from *input_relation_1* and
         *input_relation_2*, and for each pair output the
         concatenation of the two tuples

   * - **Set union, difference, and intersection**
   * - *input_relation_1* ``\union`` *input_relation_2*
         output the union of *input_relation_1* and *input_relation_2*

       *input_relation_1* ``\diff`` *input_relation_2*
         output the set difference of *input_relation_1* and
         *input_relation_2*

       *input_relation_1* ``\intersect`` *input_relation_2*
         output the intersection of *input_relation_1* and
         *input_relation_2*

   * - **Rename**
   * - ``\rename_{``\ *new_attr_names*\ ``}`` *input_relation*
         output the same *input_relation* but with attributes renamed
         to *new_attr_names*

       ``\rename_{``\ *new_rel_name*\ ``: *}`` *input_relation*
         output the same *input_relation* but rename it to
         *new_rel_name*

       ``\rename_{`` *new_rel_name* ``:`` *new_attr_names*  ``}`` *input_relation*
         output the same *input_relation* but rename it to
         *new_rel_name* and its attributes to *new_attr_names*

   * - **Aggregation** (not in standard relational algebra)
   * - ``\aggr_{``\ *aggr_attr_list*\ ``}`` *input_relation*
         output a single tuple, whose attributes are computed over the
         entire *input_relation* according to the aggregate
         expressions in *aggr_attr_list*

       ``\aggr_{``\ *group_by_attrs*\ ``:`` *aggr_attr_list*\ ``}`` *input_relation*
         partition *input_relation* in to groups of tuples according
         to *aggr_attr_list*, and then for each group, output a tuple
         whose attributes are computed over the group according to the
         aggregate expressions in *aggr_attr_list*

Writing Relational Algebra Queries
----------------------------------

* End every query with a semicolon (``;``).

* The simplest query is one that returns a database relation, i.e.:
  *relation_name*\ ``;``

* Build a complex query by nesting: you can feed a subquery as an
  input relation to another relational operator (using parentheses to
  enclose the subquery as necessary to avoid ambiguity) , e.g.:
  ``\select_{``\ *condition*\ ``} (\project_{``\ *attr_list*\ ``}``
  *input_relation_1* ``) \join`` *input_relation_2* ``;``

Commands
--------

.. list-table::
   :header-rows: 0

   * - ``\quit;``
     - Exit from RA
   * - ``\list;``
     - List database relations and user-defined views
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

