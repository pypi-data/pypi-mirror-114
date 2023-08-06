# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['simple_sqla_timer']
install_requires = \
['SQLAlchemy>=1.3.19,<2.0.0']

setup_kwargs = {
    'name': 'simple-sqla-timer',
    'version': '0.1.0',
    'description': 'A simple way of logging how long it takes for SQLAlchemy queries to run.',
    'long_description': '[![Formatter](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Build Status](https://github.com/Barbora-Data-Science/simple-sqla-timer/actions/workflows/main.yml/badge.svg)](https://github.com/Barbora-Data-Science/simple-sqla-timer/actions/workflows/main.yml)\n[![codecov](https://codecov.io/gh/Barbora-Data-Science/simple-sqla-timer/branch/main/graph/badge.svg?token=MJSSVCSFJV)](https://codecov.io/gh/Barbora-Data-Science/simple-sqla-timer)\n[![PyPI version](https://badge.fury.io/py/simple-sqla-timer.svg)](https://pypi.org/project/simple-sqla-timer/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/simple-sqla-timer)](https://pypi.org/project/simple-sqla-timer/)\n\n\n# Description\nProvides a simple way to find slow SQL queries when using SQLAlchemy.\n\nHooks into the SQLAlchemy events system to find when queries start and finish.\nNote that this is not meant to serve as a profiler and will not explain why your queries are slow,\njust tell you which ones are.\nSee [SQLAlchemy docs about performance](https://docs.sqlalchemy.org/en/14/faq/performance.html) \nfor profiling if you need to find out how much time a query spends waiting for database response,\nfetching the data and ORM operations.\n\n# Installation\n\nThis is a pure python package, so it can be installed with `pip install simple-sqla-timer` \nor any other dependency manager.\n\n# Usage\n\nRun this function at the start of your application:\n```python\nfrom simple_sqla_timer import setup_query_timer\n\nsetup_query_timer()\n```\nBy default, this will log the start of the statements and their durations to the `simple_sqla_timer` logger, with \n`debug` level. You can override this behaviour by specifying a custom logging function:\n```python\nimport logging\nfrom simple_sqla_timer import setup_query_timer\n\ndef my_log_function(statement: str, duration: float) -> None:\n    logging.info("Query: %s\\nDuration:%f", statement, duration)\n\nsetup_query_timer(my_log_function)\n```\n__Important__: The query timer *must* be set up *before* the application opens SQLAlchemy `Engine` connections. Any \nconnections opened before setting up the timer will not have their statements logged.\n\n# Development\n\nThis library uses the [poetry](https://python-poetry.org/) package manager, which has to be installed before installing\nother dependencies. Afterwards, run `poetry install` to create a virtualenv and install all dependencies.\n\n[Black](https://github.com/psf/black) is used (and enforced via workflows) to format all code. Poetry will install it\nautomatically, but running it is up to the user. To format the entire project, run `black .`.\n\n# Contributing\n\nThis project uses the Apache 2.0 license and is maintained by the data science team @ Barbora. All contributions are \nwelcome in the form of PRs or raised issues.\n',
    'author': 'Saulius Beinorius',
    'author_email': 'saulius.beinorius@gmail.com',
    'maintainer': 'Saulius Beinorius',
    'maintainer_email': 'saulius.beinorius@gmail.com',
    'url': 'https://github.com/Barbora-Data-Science/simple-sqla-timer',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
