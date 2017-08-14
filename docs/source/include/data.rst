Data Types and Operators
------------------------

RA knows about five basic value types: ``boolean``, ``number``,
``string``, ``date``, and ``datetime``.  It doesn't distinguish
integers vs. floats, or fixed- vs. variable-length strings.

.. note:: RA also uses two special types ``unknown`` and ``any``; see
   :ref:`Type Checking` below for how they are useful.

Literals
^^^^^^^^

As with SQL, string literals are enclosed in single quotes, e.g.,
``'Amy'``.  If you need to include the single-quote character itself
in a string literal, use two in a row, e.g., ``'Alivia''s Durham
Bistro'``.

You can enter ``date`` and ``datetime`` literals as strings (e.g.,
``'1975-01-01'`` and ``'2017-06-01 21:00:00'``); RA relies on the
underlying database system to convert them implicitly into ``date``\ s
and ``datetime``\ s (see :ref:`Type Checking` below).

Operators and Functions
^^^^^^^^^^^^^^^^^^^^^^^

* Comparison operators ``<``, ``<=``, ``=`` (equal), ``<>`` (not
  equal), ``>=``, and ``>`` work for pairs of ``number``\ s,
  ``string``\ s, ``date``\ s, or ``datetime``\ s, and return a
  ``boolean``.

* Arithmetic operators ``+``, ``-``, ``*``, and ``/`` work on a pair
  of ``number``\ s, and return a ``number``.

* Concatenation operator ``||`` works on two ``string``\ s and returns
  a ``string``.

* Boolean operators ``and``, ``or``, and ``not`` work on ``boolean``
  values and return a ``boolean`` value.

* As in SQL, operator ``like`` matches a ``string`` against a pattern
  (represented as a ``string``).  For example, ``bar.name like 'A%'``
  returns true if ``bar.name`` starts with "``A``" (``%`` in a pattern
  matches any sequence of 0 or more characters).

The list above is not exhaustive.  For more details, please refer to
the declarations in the ``default_functions`` setting in the
:codeurl:`default configuration file </radb/sys.ini>` (this file is
not meant to be modified by users); see :ref:`Specification of
Built-in Functions` for the format of these declarations.

In addition to the operators above, RA also supports functions with
the standard syntax of *func_name*\ ``(``\ *arg_1*\ ``,`` *arg_2*\
``,`` ... ``)``.  For example, RA on top of PostgreSQL understands
``now()`` (which returns the current ``datetime``) and ``ceil(1.618)``
(which returns the ceiling of 1.618).  Despite the SQL standard,
different database vendors support different SQL functions.  For the
most part, RA simply translates these function calls verbatim to SQL.
However, you can declare a list of functions supported by a specific
database vendor in a configuration file (again, see
:ref:`Specification of Built-in Functions` for details) so RA can
provides additional type-checking (see :ref:`Type Checking` below).

Type Checking
^^^^^^^^^^^^^

RA assumes that an operator or function takes a number of values as
input arguments, and returns a single value as output.  Required
arguments (possibly none) always come first, followed by optional ones
(possibly none).  Finally, a function can be declared to take an
arbitrary number of additional arguments beyond those listed; these
additional arguments all must have the same type as the last one
listed.

Here are some examples (see :ref:`Specification of Built-in Functions`
for exact syntax and where to specify them):

``now() -> datetime``

  This function takes no input arguments and returns a single
  ``datetime`` value.

``substr(string, number, number?) -> string``

  This function takes a string and a number as its required arguments,
  and another number as its optional third argument, as indicated by
  the ``?`` suffix; the function returns a string.

``greatest(number, number, number*) -> number``

  This function takes two or more numbers as input arguments, and
  returns a number.  Here, ``*`` indicates zero or more occurrences.

``foo(date, string?, number?, any*) -> number``

  This toy example specifies a function with a required date input
  argument, optionally followed by a string, a number, and then any
  number of additional parameters with any type.  Here, ``any`` is
  special type to which all data types conform to.

On a high level, RA type-checks each use of operator/function in a
query against known declarations.  Several rules are worth noting.

**Implicit type conversions**

  RA assumes that the underlying database system can automatically
  convert ``datetime`` to ``date`` values, and convert ``string`` to
  ``date`` and ``datetime`` values.  Therefore, RA is able to deduce
  that ``drinker.dob <= '1975-01-01'`` (where attribute
  ``drinker.dob`` has type ``date``) is a valid comparison, because
  ``'1975-01-01'`` can be converted to a ``date``.  If the ``string``
  value doesn't translate to a valid ``date``, RA relies on the
  underlying database system to catch the error at run time.

**Positional arguments**

  RA assumes that arguments are "positional."  In other words, for
  each argument type listed in a declaration, RA expects an argument
  of a conforming type at the same position.  Consequently, if you
  want to supply a optional argument, then all arguments preceding it
  in the declaration (including optional arguments) must be supplied.
  For example, ``foo('1975-01-01', 'Watergate', 1)`` conforms to the
  declaration of ``foo`` above, while ``foo('1975-01-01', 1)`` does
  not.

**Polymorphic operators/functions**

  In general, RA allows each operator/function to have multiple
  signatures.  Based on the order in which they appear in
  configuration files (see :ref:`Specification of Built-in Functions`
  for details), these declarations are organized as a list.  To check
  an invocation, RA walks down this list.  As soon as a RA encounters
  a declaration that this invocation's input arguments conform to, RA
  considers the invocation to be correct and assumes that its return
  type is the one associated with that declaration.

  .. warning:: An implication of this overly simplistic rule is that
     the order of declaration matters, unfortunately, sometimes in
     subtle way.  For example, in the sample :codeurl:`configuration
     file for PostgreSQL</sample/postgresql.ini>`, declarations for
     ``+`` are listed in the following order::

       PLUS(number, number) -> number
       PLUS(date, number) -> date      # here number means the number of days
       PLUS(number, date) -> date      # ditto

     Suppose, for the sake of argument, that an implicit conversion
     from ``number`` to ``date`` is possible (it is *not* in RA).
     Then, had we instead listed ``PLUS(date, number)`` before
     ``PLUS(number, number)``, RA would infer that ``1+2`` returns a
     ``date``!

     A perhaps better alternative for a future version of RA would be
     a picking the declaration that "best fits" the given invocation
     (i.e., requiring the least amount of implicit type conversion).

**Unrecognized functions/SQL types**

  If RA encounters a function *f* that it doesn't know about, it
  assumes that *f* can take any number of arguments of any type, and
  that *f* returns a value of special type ``unknown``.  Type
  ``unknown`` is also used when RA encounters an exotic SQL type that
  it doesn't know (e.g., a user-defined type for some database
  column).  RA assumes Type ``unknown`` can be implicitly converted to
  any other type.  This rule is extremely lenient by design, because
  different database vendors support many, many different built-in
  functions that would be impossible for RA to track.  This rule
  essentially allows RA to pass on such expressions to the underlying
  database system, which will eventually check them in SQL.
