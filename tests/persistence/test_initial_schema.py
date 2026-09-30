import pytest
import sqlite3

from app.infrastructure.persistence.database import Database
from app.infrastructure.persistence.migrations.registry import MIGRATIONS
from app.infrastructure.persistence.migrations.runner import MigrationRunner

EXPECTED_TABLES = {
    "schema_version",
    "muscle_groups",
    "exercises",
    "exercise_sessions",
    "exercise_entries",
    "exercise_sets",
    "cardio_sessions",
    "weight_records",
    "routine_templates",
    "routine_variants",
    "routine_exercises",
    "routine_sets",
    "recommendations",
    "rest_records",
    "exercise_rules",
}

def test_initial_schema_creates_expected_tables(tmp_path):
    database = Database(tmp_path / "test.db")
    runner = MigrationRunner(database, MIGRATIONS)

    runner.initialize()

    with database.transaction() as connection:
        rows = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    actual_tables = {row["name"] for row in rows}

    assert EXPECTED_TABLES.issubset(actual_tables)

def test_initial_schema_records_version(tmp_path):
    database = Database(tmp_path / "test.db")
    runner = MigrationRunner(database, MIGRATIONS)

    runner.initialize()

    with database.transaction() as connection:
        row = connection.execute(
            """
            SELECT version, name
            FROM schema_version
            WHERE version = 1
            """
        ).fetchone()

    assert row is not None
    assert row["version"] == 1
    assert row["name"] == "initial_schema"

def test_initial_schema_enforces_foreign_keys(tmp_path):
    database = Database(tmp_path / "test.db")
    runner = MigrationRunner(database, MIGRATIONS)
    runner.initialize()

    with pytest.raises(sqlite3.IntegrityError):
        with database.transaction() as connection:
            connection.execute(
                """
                INSERT INTO exercise_entries (
                    id, session_id, exercise_id, exercise_order
                ) VALUES ('e1', 'nonexistent_session', 'nonexistent_exercise', 1)
                """
            )







