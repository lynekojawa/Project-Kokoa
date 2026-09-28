"""This module owns SQLite connection management and transaction handling"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing  import Iterator

class Database:
    """Manage SQLite connections and transactions."""

    def __init__(self, db_path: str| Path)-> None:
        self.db_path = Path(db_path)

        if str(self.db_path) != ":memory:":
            self.db_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

    def _connect(self) -> sqlite3.Connection:
        """Open a connection for internal use"""
        connection = sqlite3.connect(
            str(self.db_path),
            timeout = 5.0
        )
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Provide a connection with automatic commit/rollback."""
        connection = self._connect()

        try:
            connection.execute("BEGIN")
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        """Initialize the database schema and apply migrations."""
        raise NotImplementedError(
            "Migration runner is not implemented yet."
        )







