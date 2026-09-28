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

    def connect(self) -> sqlite3.Connection:
        """Create a configured SQLite connection."""
        connection = sqlite3.connect(
            str(self.db_path),
            timeout = 5.0
        )

        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def transaction(
            self,
    ) -> Iterator[sqlite3.Connection]:
        """Run database operations in one transaction."""
        connection = self.connect()

        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self) -> None:
        """Initialize or migrate the database."""
        #Migration runner will be implemented next.
        raise NotImplementedError(
            "Migration runner is not implemented yet."
        )







