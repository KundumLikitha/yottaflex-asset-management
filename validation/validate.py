from database.db import get_connection
from logic.exception_detection import detect_exceptions


def generate_validation_report():
    checks = []

    with get_connection() as connection:

        # 1. Record counts
        tables = [
            "assets",
            "shipments",
            "custody_events",
            "return_authorizations",
            "inspections",
            "repairs",
            "deposit_ledger"
        ]

        print("\n========== DATA COUNTS ==========")

        for table in tables:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

            print(f"{table}: {count}")

        # 2. Primary key checks
        duplicate_assets = connection.execute("""
            SELECT asset_id
            FROM assets
            GROUP BY asset_id
            HAVING COUNT(*) > 1
        """).fetchall()

        checks.append(("Asset primary keys", len(duplicate_assets) == 0))

        # 3. Foreign key checks
        foreign_key_errors = connection.execute(
            "PRAGMA foreign_key_check"
        ).fetchall()

        checks.append(("Foreign key relationships",
                       len(foreign_key_errors) == 0))

        # 4. Required field checks
        missing_asset_ids = connection.execute("""
            SELECT COUNT(*)
            FROM assets
            WHERE asset_id IS NULL OR asset_id = ''
        """).fetchone()[0]

        checks.append(("Required asset IDs", missing_asset_ids == 0))

        # 5. Invalid dates
        invalid_dates = connection.execute("""
            SELECT COUNT(*)
            FROM custody_events
            WHERE date(event_date) IS NULL
        """).fetchone()[0]

        checks.append(("Custody event dates", invalid_dates == 0))

    # 6. Exception detection
    exceptions = detect_exceptions()

    print("\n========== VALIDATION RESULTS ==========")

    for name, passed in checks:
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("\nDetected exception scenarios:", len(exceptions))

    for exception in exceptions:
        print("-", exception)

    print("\nOverall validation:",
          "SUCCESS" if all(passed for _, passed in checks)
          and len(exceptions) == 5 else "REVIEW REQUIRED")

    print("========================================")


if __name__ == "__main__":
    generate_validation_report()