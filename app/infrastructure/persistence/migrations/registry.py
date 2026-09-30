"""Central registry of database migrations."""
from importlib import import_module
from app.infrastructure.persistence.migrations.runner import Migration

_initial_schema = import_module(
    "app.infrastructure.persistence.migrations.001_initial_schema"
)

#Add new migrations here in version order.
#Never remove or reorder existing entries.
MIGRATIONS = (
    Migration(
        version=1,
        name="initial_schema",
        apply=_initial_schema.apply,
    ),
)