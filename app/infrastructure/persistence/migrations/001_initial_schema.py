"""Initial database schema for the health app."""

import sqlite3

def apply(connection: sqlite3.Connection)->None:
    """Create all initial tables and indexes."""

    statements = [
        # --------------------------------------------------
        # Exercise catalog
        # --------------------------------------------------
        """
        CREATE TABLE muscle_groups (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            priority INTEGER NOT NULL,
            active INTEGER NOT NULL DEFAULT 1
                CHECK (active IN (0,1))
        )
        """,
        """
        CREATE TABLE exercises (
            if TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            muscle_group_id TEXT NOT NULL,
            category TEXT NOT NULL,
            equipment TEXT,
            active INTEGER NOT NULL DEFAULT 1
                CHECK (active IN (0,1)),
            FOREIGN KEY (muscle_group_id)
                REFERENCES muscle_groups(id)
        )
        """,
        # --------------------------------------------------
        # Completed strength sessions
        # --------------------------------------------------
        """
        CREATE TABLE exercise_sessions (
            id TEXT PRIMARY KEY,
            data TEXT NOT NULL,
            duration_minutes REAL NOT NULL
                CHECK (duration_minutes > 0),
            notes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE exercise_entries (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            exercise_id TEXT NOT NULL,
            exercise_order INTEGER NOT NULL,
                CHECK (exercise_order > 0),
            rest_seconds INTEGER NOT NULL DEFAULT 30
                CHECK (rest_seconds 0 AND 45),
            notes TEXT,
            FOREIGN KEY (session_id)
                REFERENCES exercise_sessions(id)
                ON DELETE CASCADE,
            FOREIGN KEY (exercise_id)
                REFERENCES exercises(id)
            UNIQUE (session_id, exercise_order)
        )
        """,
        """
        CREATE TABLE exercise_sets (
            id TEXT PRIMARY KEY,
            exercise_entry_id TEXT NOT NULL,
            set_number INTEGER NOT NULL,
                CHECK (set_number > 0),
            repetitions INTEGER NOT NULL
                CHECK (repetitions > 0),
            weight REAL NOT NULL DEFAULT 0
                CHECK (weight >= 0),
            unit TEXT NOT NULL
                CHECK (unit IN ('kg', 'lb')
            FOREIGN KEY (exercise_entry_id)
                REFERENCES exercise_entries(id)
                ON DELETE CASCADE
            UNIQUE (exercise_entry_id, set_number)
        )
        """,
        # --------------------------------------------------
        # Recommendations and rest records
        # --------------------------------------------------
        """
        CREATE TABLE recommendations(
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            recommendation_type TEXT NOT NULL
                CHECK (
                    recommendation_type IN (
                        'strength', 'swim', 'walk', 'rest'
                    )
                ),
            routine_variant_id TEXT,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK (
                    status IN (
                        'pending', 'completed', 'rest',
                        'different_activity'
                    )
                ),
            reason_codes TEXT,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (routine_variant_id)
                REFERENCES routine_variants(id)
        )
        """,
        """
        CREATE TABLE rest_records (
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            reason TEXT NOT NULL,
                CHECK (
                    reason IN (
                        'planned', 'recovery', 'thunderstorm',
                        'period', 'social', 'other'
                    )
                ),
            notes TEXT,
            create_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )
        """,
        # --------------------------------------------------
        # Configurable exercise rules
        # --------------------------------------------------
        """
        CREATE TABLE exercise_rules (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            rule_type TEXT NOT NULL,
            priority INTEGER NOT NULL DEFAULT 0,
            enabled INTEGER NOT NULL DEFAULT 1
                CHECK (enabled IN (0,1)),
            configuration TEXT NOT NULL DEFAULT '{}',
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        """,
        # --------------------------------------------------
        # Indexes for common date and relationship queries
        # --------------------------------------------------
        """
        CREATE INDEX idx_exercise_sessions_date
        ON exercise_sessions (date)
        """,
        """
        CREATE INDEX idx_exercise_entries_session
        ON exercise_entries (session_id)
        """,
        """
        CREATE INDEX idx_exercise_entries_exercise
        ON exercise_entries(exercise_id)
        """,
        """
        CREATE INDEX idx_cardio_sessions_date
        ON cardio_sessions(date)
        """,
        """
        CREATE INDEX idx_weight_records_date
        ON weight_records(date)
        """,
        """
        CREATE INDEX idx_recommendations_date
        ON recommendations(date)
        """,
        """
        CREATE INDEX idx_rest_records_date
        ON rest_records(date
        """,
    ]

    for statement in statements:
        connection.execute(statement)














