import json
import sqlite3
import csv
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "asset_management.db"
EXPORT_DIR = BASE_DIR / "exports"

EXPORT_DIR.mkdir(exist_ok=True)

def export_data():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    tables = connection.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """).fetchall()

    all_data = {}

    for table_row in tables:
        table = table_row["name"]

        rows = connection.execute(
            f'SELECT * FROM "{table}"'
        ).fetchall()

        records = [dict(row) for row in rows]
        all_data[table] = records

        # CSV export
        if records:
            csv_path = EXPORT_DIR / f"{table}.csv"

            with open(csv_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=records[0].keys()
                )
                writer.writeheader()
                writer.writerows(records)

        print(f"Exported {table}: {len(records)} records")

    # Combined JSON export
    json_path = EXPORT_DIR / "asset_management.json"

    with open(json_path, "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=2)

    # SQL export
    sql_path = EXPORT_DIR / "asset_management.sql"

    with open(sql_path, "w", encoding="utf-8") as file:
        for statement in connection.iterdump():
            file.write(statement + "\n")

    connection.close()

    print("\nCSV, JSON and SQL exports completed!")
    print("Export folder:", EXPORT_DIR)


if __name__ == "__main__":
    export_data()