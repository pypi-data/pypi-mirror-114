"""SQL query timing logic."""

import logging
import time
from functools import partial
from typing import Any, Callable

import sqlalchemy
from sqlalchemy import event

LogFunction = Callable[[str, float], None]

LOGGER = logging.getLogger(__name__)


def _cut_if_too_long(text: str, max_length: int) -> str:
    """Cut a string down to the maximum length.

    Args:
        text: Text to check.
        max_length: The maximum length of the resulting string.

    Returns:
        Cut string with ... added at the end if it was too long.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def _default_logger(statement: str, duration: float, max_query_length=100) -> None:
    """Default version of the logging function.

    Logs the SQL query (trimmed if long, which is almost always) and it's duration in seconds.

    Args:
        statement: SQL text of the query we are logging duration for.
        duration: How long the query took, in seconds.
    """
    LOGGER.debug(
        "SQL query %s took %f seconds",
        _cut_if_too_long(statement, max_query_length),
        duration,
    )


def _add_start_time(conn: sqlalchemy.engine.Connection, **_kwargs: Any) -> None:
    """Adds the query start time to a single connection's information.

    Args:
        conn: Connection to add the start time to (the one executing the query).
        **_kwargs: Other unused arguments.
    """
    conn.info.setdefault("query_start_time", []).append(time.perf_counter())


def _log_time_taken(
    conn: sqlalchemy.engine.Connection,
    statement: str,
    log_function: LogFunction,
    **_kwargs: Any
) -> None:
    """Checks the connection information to calculate and log the time taken for the query.

    Args:
        conn: Connection that executed the query (should have the query_start_time added).
        statement: SQL query that was executed.
        **_kwargs: Other unused arguments.
    """
    duration = time.perf_counter() - conn.info["query_start_time"].pop(-1)
    log_function(statement, duration)


def setup_query_timer(log_function: LogFunction = _default_logger) -> None:
    """Sets up event listeners required to be able to calculate how long each SQL query takes.

    See Also:
        https://docs.sqlalchemy.org/en/14/core/event.html
        https://docs.sqlalchemy.org/en/14/core/events.html
    """
    # named=True allows us to ignore all arguments of the listeners that we don't care about
    event.listen(
        sqlalchemy.engine.Engine, "before_cursor_execute", _add_start_time, named=True
    )
    event.listen(
        sqlalchemy.engine.Engine,
        "after_cursor_execute",
        partial(_log_time_taken, log_function=log_function),
        named=True,
    )
