# sqla-wrapper

A friendly wrapper for [modern SQLAlchemy](https://docs.sqlalchemy.org/en/14/glossary.html#term-2.0-style) (v1.4 or later) and Alembic.

Includes:

- A `SQLAlchemy` wrapper, that does all the SQLAlchemy setup and gives you:
    - A preconfigured scoped session.
    - A model baseclass including some helper methods.
    - A helper for performant testing with a real database

- An `Alembic` wrapper that loads the config from your application instead of an ini file.

- A `sa` helper module, that imports all the functions and classes from `sqlalchemy`and `sqlalchemy.orm`,
so you don't need to repeat those imports everywhere.

## Resources

- [Documentation](https://sqla-wrapper.jpscaletti.com)
- [PyPI](https://pypi.org/project/sqla-wrapper/)
- [Change log](https://github.com/jpsca/sqla-wrapper/releases)
