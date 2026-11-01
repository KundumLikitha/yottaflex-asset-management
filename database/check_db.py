from database.db import get_connection

with get_connection() as connection:
    tables = [
        "asset_types",
        "owners",
        "locations",
        "assets",
        "shipments",
        "shipment_assets",
        "custody_events"
    ]

    print("\nDatabase record counts:")
    for table in tables:
        count = connection.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]
        print(f"{table}: {count}")