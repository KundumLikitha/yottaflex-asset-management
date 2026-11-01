import random
from datetime import datetime, timedelta

from faker import Faker
from database.db import get_connection

fake = Faker()
SEED = 20261022

random.seed(SEED)
Faker.seed(SEED)

def generate_master_data():

    with get_connection() as connection:

        # 1. Asset types
        asset_types = [
            ("TYPE-001", "PALLET", "Reusable wooden or plastic pallets"),
            ("TYPE-002", "CONTAINER", "Reusable shipping containers"),
            ("TYPE-003", "CRATE", "Reusable storage crates"),
            ("TYPE-004", "DRUM", "Reusable industrial drums"),
            ("TYPE-005", "TROLLEY", "Reusable material handling trolleys")
        ]

        connection.executemany("""
            INSERT OR IGNORE INTO asset_types
            (asset_type_id, type_name, description)
            VALUES (?, ?, ?)
        """, asset_types)

        # 2. Owners
        owners = []

        owner_types = ["COMPANY", "SUPPLIER", "CUSTOMER"]

        for i in range(1, 21):
            owners.append((
                f"OWN-{i:04d}",
                fake.company(),
                random.choice(owner_types)
            ))

        connection.executemany("""
            INSERT OR IGNORE INTO owners
            (owner_id, owner_name, owner_type)
            VALUES (?, ?, ?)
        """, owners)

        # 3. Locations
        locations = []

        for i in range(1, 16):
            locations.append((
                f"LOC-{i:04d}",
                f"{fake.city()} Warehouse",
                fake.city(),
                fake.country()
            ))

        connection.executemany("""
            INSERT OR IGNORE INTO locations
            (location_id, location_name, city, country)
            VALUES (?, ?, ?, ?)
        """, locations)

        # 4. Reusable assets
        assets = []

        for i in range(1, 20001):

            asset_type_id = random.choice(asset_types)[0]
            owner_id = random.choice(owners)[0]

            created_date = datetime(2025, 1, 1) + timedelta(
                days=random.randint(0, 365)
            )

            assets.append((
                f"ASSET-{i:07d}",
                asset_type_id,
                owner_id,
                f"SN-{i:07d}",
                "AVAILABLE",
                created_date.strftime("%Y-%m-%d %H:%M:%S")
            ))

        connection.executemany("""
            INSERT OR IGNORE INTO assets
            (asset_id, asset_type_id, owner_id, serial_number,
             current_status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, assets)

    print("Master data generated successfully!")
    print("Asset types:", len(asset_types))
    print("Owners:", len(owners))
    print("Locations:", len(locations))
    print("Reusable assets:", len(assets))


if __name__ == "__main__":
    generate_master_data()