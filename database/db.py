import sqlite3
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = BASE_DIR / "database"
DB_PATH = DATABASE_DIR / "asset_management.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"


def get_connection():
    """Create a database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    """Create database tables using schema.sql."""
    DATABASE_DIR.mkdir(exist_ok=True)

    schema = SCHEMA_PATH.read_text(encoding="utf-8")

    with get_connection() as connection:
        connection.executescript(schema)

    print("Database initialized successfully!")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    initialize_database()