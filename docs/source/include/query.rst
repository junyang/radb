Writing Queries
---------------

Relation Schema and Attribute References
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note:: Before delving into details, let's start with a bit of
   motivation.  The relational model in its purest form requires
   *distinct* attribute names within each relation (because a tuple is
   considered as a function from attribute names to values), including
   result relations returned by relational algebra expressions;
   therefore, each attribute can be referenced uniquely by its name.
   In practice, however, to simplify expressions, RA (as well as most
   textbooks and courses that cover relational algebra) allows
   duplicate attribute names and, in case of confusion, allows them to
   be distinguished by prefixing them with names of relations where
   they come from, e.g.::

     Drinker \join_{Drinker.name=Frequents.drinker} Frequents;

     \select_{Drinker.name=Frequents.drinker}
       (Drinker \cross Frequents);

   However, the notion of "relations where they come from" needs
   clarification when inputs to an operator are themselves complex
   queries.  Moreover, it is possible for attributes to become
   indistinguishable even if we qualify them with relation names,
   e.g., in the output of ``Drinker \cross Drinker;``.

   Furthermore, the projection operator in relational algebra is often
   extended to allow output attributes computed by expressions.  It is
   not always obvious how to name such output attributes; as a result,
   it may become impossible to refer to refer to such an attribute by
   name.

   Therefore, we need to clarify how relation schema and attribute
   references work in RA.

In RA, a relation can a stored database relation, or the result of
executing a relational algebra query (or subquery).  The schema of the
relation is a list of attribute specifications, while each attribute
specification is a triple (*rel_name*, *attr_name*, *attr_type*).
Intuitively, *rel_name* is the name of the relation where this
attribute originally comes from.  Both *rel_name* and *attr_name* can
be optional.  Within a relation, there is no requirement that
*attr_name*\ s, or even (*rel_name*, *attr_name*) pairs, are unique.

Some relational operators allow you to write expressions involving
references to attributes in input relations.  An attribute reference
must be in one of the following forms:

* *attr_name* (just the attribute name by itself);

* *rel_name*\ ``.``\ *attr_name* (attribute name prefixed by
  relational name).

For an attribute reference in an operator to be valid, there
must be exactly one attribute specification in the input relation
schema(s) matching the reference.  If there are more than one matching
attribute specifications (possibly from different input relation
schemas), the attribute reference is ambiguous.

For a stored database relation, RA uses its column names and types for
the attribute specifications (mapping SQL data types to RA ones as
appropriate; see :ref:`Data Types and Operators`); the *rel_name*\ s
get the name of the database table.

The section on :ref:`Relational Algebra Operators` will further spell
out how each relational operator generates its output relation schema
from the input relation schema(s).  In general, attribute names may no
longer stay unique, and you may lose the ability to distinguish or
reference certain attributes.

If you turn on the verbose option (``-v``; see :ref:`Command-Line
Options`) when running RA, RA will print out an operator tree for your
query and show the schema for each result relation (intermediate or
final).

Relational Algebra Operators
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This section will not define what these operators do on data---see
:ref:`Basic Usage` or refer to standard textbooks.  Here, we instead
focus on issues more specific to RA.

**Selection**: ``\select_{``\ *condition*\ ``}`` *input_relation*

  Here, *condition* must have type `boolean`.  The output relation
  schema is the same as the input one.

**Projection**: ``\project_{``\ *attr_list*\ ``}`` *input_relation*

  Here, *attr_list* is a comma-separated list of expressions that
  specifies the output attributes.  The output relational schema is
  the list of output attribute specification, ordered according to
  *attr_list*.  For an output attribute, if its expression is simply
  an attribute reference, its specification will be the same as the
  specification of the input attribute being referenced.  Otherwise,
  the output attribute specification will have no relation name or
  attribute name, and its type will be what RA infers for the
  expression.

**Theta-Join**: *input_relation_1* ``\join_{``\ *cond*\ ``}`` *input_relation_2*

  Here, *condition* must have type `boolean`.  The output relation
  schema is the concatenation of the two input relation schemas.  RA
  will warn if some attribute from the first input can be potentially
  confused with some attribute from the second input, which may create
  a problem when you want to refer to them later in the join output.
  (Here, RA only warns about ambiguity caused by the join; if either
  input already contains ambiguously named attributes by itself, they
  would have been caught and reported earlier.)

**Natural join**: *input_relation_1* ``\join`` *input_relation_2*

  RA looks for matches of pairs of attributes---one from each
  input---with identical (and non-optional) names.  RA will generate
  an error if an attribute is involved in more than one match, or the
  two attributes involved in a match have types that cannot be
  equated.  If no matches are found, natural join degenerates into
  cross product, and RA will generate a warning.

  For each pair of matching attributes, RA equates them in the join.
  The output relation schema consists of all attribute specifications
  from *input_relation_1*, followed by those from *input_relation_2*
  that are not involved in any match.  Consequently, you can still
  refer to a join attribute by name in the output relation, but
  prefixing it with the name of *input_relation_2* won't work any more
  (incidentally, prefixing it with the name of *input_relation_1*
  would still work, but it is not recommended).

**Cross product**: *input_relation_1* ``\cross`` *input_relation_2*

  The output relation schema is the concatenation of the two input
  relation schemas.  Again, as with the case of theta-join, RA will
  warn if some attribute from the first input can be potentially
  confused with some attribute from the second input.

**Set union, difference, and intersection**:

  *input_relation_1* ``\union`` *input_relation_2*

  *input_relation_1* ``\diff`` *input_relation_2*

  *input_relation_1* ``\intersect`` *input_relation_2*

  Two input relations must have the same number of attributes and
  every pair of corresponding attributes must have identical types
  (which is a stronger condition than being able to equate them).  RA
  will warn if some pair of corresponding attributes have different
  names.

  The output relation schema consists of all attribute specifications
  from *input_relation_1*.  Consequently, you can still refer to
  attributes by their names from the first input relation, but you
  lose the ability of referring them by names from the second input
  relation.  (Allowing the later would necessitate remembering
  multiple possible names for each output attribute, which can get
  quite confusing; for this reason, RA adopts the convention of always
  going with the first input relation.)

**Rename**:

  ``\rename_{``\ *new_attr_names*\ ``}`` *input_relation*

  ``\rename_{``\ *new_rel_name* ``: *}`` *input_relation*

  ``\rename_{`` *new_rel_name* ``:`` *new_attr_names* ``}`` *input_relation*

  The output relation schema consists of all attribute specifications
  from *input_relation*.  If *new_rel_name* is given, the relation
  name for all attribute specifications will set to *new_rel_name*;
  otherwise the relation name will be unset (the relation names from
  the input schema will be forgotten).  If *new_attr_names* is given,
  it will be used to set the attribute names in the output attribute
  specifications; otherwise the attribute names from the input
  relation will be retained.
