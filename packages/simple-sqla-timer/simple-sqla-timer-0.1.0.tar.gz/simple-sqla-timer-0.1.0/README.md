[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://github.com/Barbora-Data-Science/simple-sqla-timer/actions/workflows/main.yml/badge.svg)](https://github.com/Barbora-Data-Science/simple-sqla-timer/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/Barbora-Data-Science/simple-sqla-timer/branch/main/graph/badge.svg?token=MJSSVCSFJV)](https://codecov.io/gh/Barbora-Data-Science/simple-sqla-timer)
[![PyPI version](https://badge.fury.io/py/simple-sqla-timer.svg)](https://pypi.org/project/simple-sqla-timer/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-sqla-timer)](https://pypi.org/project/simple-sqla-timer/)


# Description
Provides a simple way to find slow SQL queries when using SQLAlchemy.

Hooks into the SQLAlchemy events system to find when queries start and finish.
Note that this is not meant to serve as a profiler and will not explain why your queries are slow,
just tell you which ones are.
See [SQLAlchemy docs about performance](https://docs.sqlalchemy.org/en/14/faq/performance.html) 
for profiling if you need to find out how much time a query spends waiting for database response,
fetching the data and ORM operations.

# Installation

This is a pure python package, so it can be installed with `pip install simple-sqla-timer` 
or any other dependency manager.

# Usage

Run this function at the start of your application:
```python
from simple_sqla_timer import setup_query_timer

setup_query_timer()
```
By default, this will log the start of the statements and their durations to the `simple_sqla_timer` logger, with 
`debug` level. You can override this behaviour by specifying a custom logging function:
```python
import logging
from simple_sqla_timer import setup_query_timer

def my_log_function(statement: str, duration: float) -> None:
    logging.info("Query: %s\nDuration:%f", statement, duration)

setup_query_timer(my_log_function)
```
__Important__: The query timer *must* be set up *before* the application opens SQLAlchemy `Engine` connections. Any 
connections opened before setting up the timer will not have their statements logged.

# Development

This library uses the [poetry](https://python-poetry.org/) package manager, which has to be installed before installing
other dependencies. Afterwards, run `poetry install` to create a virtualenv and install all dependencies.

[Black](https://github.com/psf/black) is used (and enforced via workflows) to format all code. Poetry will install it
automatically, but running it is up to the user. To format the entire project, run `black .`.

# Contributing

This project uses the Apache 2.0 license and is maintained by the data science team @ Barbora. All contributions are 
welcome in the form of PRs or raised issues.
