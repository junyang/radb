RA (``radb``): A relational algebra interpreter over relational databases
=========================================================================

RA is a simple relational algebra interpreter written in Python 3.  It
is built on top of an SQL-based relational database system.  It
implements relational algebra queries by translating them into SQL and
executing them on the underlying database system through `SQLAlchemy
<http://www.sqlalchemy.org/>`_.  RA is packaged with `SQLite
<http://sqlite.org/>`_, so you can use RA as a standalone
relational-algebra database system.  Alternatively, you can use RA as
a relational-algebra front-end to connect to other database servers
from various vendors.

You can follow the `project <https://github.com/junyang/radb>`_ on
GitHub, or read its documentation `here
<http://www.cs.duke.edu/~junyang/radb>`_.
