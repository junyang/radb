Basic Usage
===========

Once you are in RA, you will see the ``ra>`` prompt.  For help, type
``\help;``.  You exit RA by issuing the ``\quit;`` command.  Use the
``\list;`` command to see what relations are available for query in
your database.

The simplest relational query you can write is one that returns the
content of a relation: Just type: *rel*\ ``;``, where *rel* is the
relation name.  Note that every query/command should be terminated by
a semicolon (``;``).

In RA, relation and attribute names are case-sensitive (although some
database systems and/or their Python drivers may let you ignore
cases).  When in doubt, always use the exact same names shown in the
output of the ``\list;`` command.  Attributes can be of a variety of
types; for details see :ref:`Data Types and Operators`.  For now just
note that RA supports numbers, strings, dates, datetimes, as well as
more exotic SQL types.

Here is an example of a complex query, which returns beers liked by
those drinkers who do not frequent James Joyce Pub::

  \project_{beer} (
    ((\project_{name}          // all drinkers
       Drinker)
     \diff
     (\rename_{name}           // rename so we can diff
        \project_{drinker}     // drinkers who frequent JJP
          \select_{bar = 'James Joyce Pub'}
            Frequents))
    \join_{drinker = name}     /* join with Likes to find beers */
    Likes
  );

RA syntax is insensitive to white space, and you can enter a query on
multiple lines. C/C++/Java-style comments (``//`` and ``/*...*/``) are
supported.

RA supports the following relational algebra operators.  In general,
*input_relation*, *input_relation_1*, etc. below can be database
relations as well as intermediate outputs produced by other relational
algebra operators.

**Selection**: ``\select_{``\ *condition*\ ``}`` *input_relation*

  For example, to select *Drinker* tuples with name Amy or Ben, we can
  write::

    \select_{name='Amy' or name='Ben'} Drinker;

  String literals should be enclosed in single quotes.  Comparison
  operators ``<=``, ``<``, ``=``, ``>``, ``>=``, and ``<>``
  (inequality) work as expected on strings, numbers, and dates.
  For
  string match you can use the `like` operator; e.g.::

    \select_{name like 'A%'} Drinker;

  finds all drinkers whose name start with "A", where ``%`` is a
  wildcard character that matches any number of characters.  Finally,
  you can use boolean connectives ``and``, ``or``, and ``not`` to
  construct more complex conditions.  More features are available; see
  :ref:`Data Types and Operators` for details.

**Projection**: ``\project_{``\ *attr_list*\ ``}`` *input_relation*

  Here, *attr_list* is a comma-separated list of expressions that
  specifies the output attributes.  For example, to find out what
  beers are served by Talk of the Town (but without the price
  information), you can write::

    \project_{bar, beer} \select_{bar='Talk of the Town'} Serves;

  You can also use an expression to compute the value of an output
  attribute; e.g.::

    \project_{bar, 'Special Edition '||beer, price+1} Serves;

  Note that ``||`` concatenates two strings.

**Theta-Join**: *input_relation_1* ``\join_{``\ *cond*\ ``}`` *input_relation_2*

  For example, to join *Drinker*\ (*name*, *address*) and *Frequents*\
  (*drinker*, *bar*, *times_a_week*) relations together using drinker
  name, you can write::

    Drinker \join_{name=drinker} Frequents;

  Syntax for *cond* is similar to the case of ``\select``.

  You can prefix references to attributes with names of the relations
  that they belong to, which is sometimes useful to avoid confusion
  (see :ref:`Relation Schema and Attribute References` for more
  details)::

    Drinker \join_{Drinker.name=Frequents.drinker} Frequents;

**Natural join**: *input_relation_1* ``\join`` *input_relation_2*

  For example, to join *Drinker*\ (*name*, *address*) and *Frequents*\
  (*drinker*, *bar*, *times_a_week*) relations together using drinker
  name, we can write ``Drinker \join \rename_{name, bar, times_a_week}
  Frequents;``. Natural join will automatically equate all pairs of
  identically named attributes from its inputs (in this case, name),
  and output only one attribute per pair. Here we use ``\rename`` to
  create two name attributes for the natural join; see notes on
  ``\rename`` below for more details.

**Cross product**: *input_relation_1* ``\cross`` *input_relation_2*

  For example, to compute the cross product of *Drinker* and
  *Frequents*, you can write::

    Drinker \cross Frequents;.

  In fact, the following two queries are equivalent::

    \select_{Drinker.name=Frequents.drinker}
      (Drinker \cross Frequents);

    Drinker \join_{Drinker.name=Frequents.drinker} Frequents;

**Set union, difference, and intersection**:

  *input_relation_1* ``\union`` *input_relation_2*

  *input_relation_1* ``\diff`` *input_relation_2*

  *input_relation_1* ``\intersect`` *input_relation_2*

  For a trivial example, the set union, difference, and intersection
  between *Drinker* and itself, should return the contents of
  *Drinker* itself, an empty relation, and again the contents of
  *Drinker* itself, respectively.

**Rename**:

  ``\rename_{``\ *new_attr_names*\ ``}`` *input_relation*

    This form of the rename operator renames the attributes of its
    input relation to those in *new_attr_names*, a comma-separated
    list of names.

  ``\rename_{``\ *new_rel_name*\ ``: *}`` *input_relation*

    This form of the rename operator gives a new relation name to its
    input relation (the attribute names remain the same).  For
    example::

      \rename_{s1:*} Serves
        \join_{s1.beer=s2.beer and s1.price>s2.price}
      \rename_{s2:*} Serves;

  ``\rename_{`` *new_rel_name* ``:`` *new_attr_names*  ``}`` *input_relation*

    This form of the rename operator allows you to rename both the
    input relation as well as its attributes.

**Aggregation and grouping**:

  This operator is not in the standard relational algebra.  It has two
  forms:

  ``\aggr_{``\ *aggr_attr_list*\ ``}`` *input_relation*

    This simple form of aggregation computes a single tuple,
    aggregated over the entire input relation.  Here, *aggr_attr_list*
    is a comma-separated list of aggregate expressions involving
    functions such as ``sum``, ``count``, ``avg``, ``min``, and
    ``max``.  For example::

      \aggr_{sum(price), avg(price)} Serves;

  ``\aggr_{``\ *group_by_attrs*\ ``:`` *aggr_attr_list*\ ``}`` *input_relation*

    With this form, the input relation is first partitioned into
    groups, according to the attributes listed in *group_by_attrs*:
    all tuples that agree on the values of *group_by_attrs* go into
    the same group.  Then, for each group, one output tuple is
    produced: it will have the values for *group_by_attrs* (which are
    shared by all group members), followed by the values of aggregate
    expressions in *aggr_attr_list*.  For example, the following query
    finds, for each beer, its average price and number of bars serving
    it::

      \aggr_{beer: avg(price), count(1)} Serves;
