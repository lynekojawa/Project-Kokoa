import pytest
from app.infrastructure.persistence.database import Database

def test_connection_enables_foreign_keys(tmp_path):
    database = Database(tmp_path/ "test.db")
    with database.transaction() as connection:
        result = connection.execute(
            "PRAGMA foreign_keys;"
        ).fetchone()[0]

    assert result == 1

def test_transaction_commits_successfully(tmp_path):
    database = Database(tmp_path /"test.db")

    with database.transaction() as connection:
        connection.execute(
            "CREATE TABLE test_records (id INTEGER PRIMARY KEY)"
        )
        connection.execute(
            "INSERT INTO test_records (id) VALUES (1)"
        )

    with database.transaction() as connection:
        result = connection.execute(
            "SELECT id FROM test_records"
        ).fetchone()

    assert result["id"] == 1

def test_transaction_rolls_back_on_error(tmp_path):
    database = Database(tmp_path / "test.db")
    with database.transaction() as connection:
        connection.execute(
            "CREATE TABLE test_records (id INTEGER PRIMARY KEY)"
        )
    with pytest.raises(RuntimeError):
        with database.transaction() as connection:
            connection.execute(
                "INSERT INTO test_records (id) VALUES (1)"
            )
            raise RuntimeError("Force rollback")
    with database.transaction() as connection:
        result = connection.execute(
            "SELECT COUNT(*) FROM test_records"
        ).fetchone()[0]
    assert result == 0




