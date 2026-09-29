import sqlite3
import pytest

from app.infrastructure.persistence.database import Database
from app.infrastructure.persistence.migrations.runner import (
    Migration,
    MigrationRunner,
)

def test_applies_migration_and_records_version(tmp_path):
    database = Database(tmp_path / "test.db")

    def create_example_table(connection):
        connection.execute(
            "CREATE TABLE example (id INTEGER PRIMARY KEY);"
        )

    runner = MigrationRunner(
        database,
        [Migration(1, "create_example", create_example_table)],
    )

    runner.initialize()

    with database.transaction() as connection:
        table = connection.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' and name = 'example'
            """
        ).fetchone()

        version= connection.execute(
            "SELECT version, name FROM schema_version"
        ).fetchone()

    assert table is not None
    assert version["version"]==1
    assert version["name"] == "create_example"

def test_does_not_apply_migration_twice(tmp_path):
    database = Database(tmp_path / "test.db")
    calls = []

    def migration(connection):
        calls.append("applied")
        connection.execute(
            "CREATE TABLE example (id INTEGER PRIMARY KEY);"
        )

    runner = MigrationRunner(
        database,
        [Migration(1, "create_example", migration)],
    )

    runner.initialize()
    runner.initialize()

    assert calls == ["applied"]

def test_failed_migration_rolls_back_schema_and_version(tmp_path):
    database = Database(tmp_path / "test.db")

    def failing_migration(connection):
        connection.execute(
            "CREATE TABLE example (id INTEGER PRIMARY KEY);"
        )
        raise RuntimeError("Simulated migration failure")

    runner = MigrationRunner(
        database,
        [Migration(1, "failing_migration", failing_migration)],
    )

    with pytest.raises(RuntimeError, match="Simulated migration failure"):
        runner.initialize()

    with database.transaction() as connection:
        table = connection.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type = 'table' AND name ='example'
            """
        ).fetchone()

        version = connection.execute(
            "SELECT version FROM schema_version"
        ).fetchall()

    assert table is None
    assert version == []

def test_rejects_duplicate_migration_versions(tmp_path):
    database = Database(tmp_path / "test.db")

    with pytest.raises(ValueError, match="unique"):
        MigrationRunner(
            database,
            [
                Migration(1, "first", lambda connection: None),
                Migration(1, "second", lambda connection: None),
            ],
        )










