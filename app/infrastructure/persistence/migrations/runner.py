from dataclasses import dataclass
from typing import Callable, Sequence
from app.infrastructure.persistence.database import Database

@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable

class MigrationRunner:
    """Apply database migrations in version order."""

    def __init__(
        self,
        database: Database,
        migrations: Sequence[Migration],
    ) -> None:
        self.database = database

        versions = [migration.version for migration in migrations]

        if any(version <= 0 for version in versions):
            raise ValueError("Migration versions must be positive.")
        if len(versions) != len(set(versions)):
            raise ValueError("Migration versions must be unique.")

        if sorted(versions) != list(range(1, len(versions) +1)):
            raise ValueError(
                "Migration versions must be sequential with no gaps."
            )

        self.migrations = tuple(
            sorted(migrations, key=lambda migration: migration.version)
        )

    def initialize(self) -> None:
        """ Create the version table and apply pending migrations"""
        with self.database.transaction() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS schema_version (
                    version INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

        for migration in self.migrations:
            with self.database.transaction()as connection:
                already_applied = connection.execute(
                    """SELECT 1
                    FROM schema_version
                    WHERE version = ?
                    """,
                    (migration.version,),
                ).fetchone()

                if already_applied:
                    continue

                migration.apply(connection)

                connection.execute(
                    """
                    INSERT INTO schema_version (version, name)
                    VALUES (?, ?)
                    """,
                    (migration.version, migration.name),
                )



