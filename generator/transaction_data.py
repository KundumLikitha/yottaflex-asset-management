import random
from datetime import datetime, timedelta
from database.db import get_connection

SEED = 20261022

def generate_transaction_data():
    rng = random.Random(SEED)

    with get_connection() as connection:
        locations = [
            row[0] for row in connection.execute(
                "SELECT location_id FROM locations ORDER BY location_id"
            )
        ]

        assets = [
            row[0] for row in connection.execute(
                "SELECT asset_id FROM assets ORDER BY asset_id"
            )
        ]

        owners = [
            row[0] for row in connection.execute(
                "SELECT owner_id FROM owners ORDER BY owner_id"
            )
        ]

        if len(assets) < 20000 or len(locations) < 2:
            raise ValueError("Generate master data first.")

        shipments = []
        shipment_assets = []
        custody_events = []

        for i in range(10000):
            shipment_id = f"SHP-2026-{i + 1:06d}"

            source = rng.choice(locations)
            destination = rng.choice(
                [loc for loc in locations if loc != source]
            )

            dispatch_date = datetime(2026, 1, 1) + timedelta(
                days=rng.randint(0, 250)
            )

            shipments.append((
                shipment_id,
                source,
                destination,
                dispatch_date.strftime("%Y-%m-%d"),
                (dispatch_date + timedelta(days=15)).strftime("%Y-%m-%d"),
                "DISPATCHED"
            ))

            # Assign two assets to each shipment
            for asset_number in range(i * 2, i * 2 + 2):
                asset_id = assets[asset_number]
                actor_id = owners[asset_number % len(owners)]

                shipment_assets.append((shipment_id, asset_id))

                # Five historical custody events per asset
                movement_locations = [
                    source,
                    destination,
                    destination,
                    source,
                    source
                ]

                movement_types = [
                    "DISPATCH",
                    "ARRIVAL",
                    "INSPECTION",
                    "RETURN",
                    "RECEIVED"
                ]

                for event_number in range(5):
                    event_date = dispatch_date + timedelta(
                        days=event_number * 2
                    )

                    custody_events.append((
                        f"CUST-{asset_id}-{event_number + 1:06d}",
                        asset_id,
                        movement_locations[event_number],
                        actor_id,
                        movement_types[event_number],
                        event_date.strftime("%Y-%m-%d")
                    ))

        connection.executemany("""
            INSERT INTO shipments
            (shipment_id, source_location_id, destination_location_id,
             dispatch_date, expected_return_date, shipment_status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, shipments)

        connection.executemany("""
            INSERT INTO shipment_assets (shipment_id, asset_id)
            VALUES (?, ?)
        """, shipment_assets)

        connection.executemany("""
            INSERT INTO custody_events
            (custody_event_id, asset_id, location_id, actor_id,
             event_type, event_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, custody_events)

    print("Transaction data generated successfully!")
    print("Shipments:", len(shipments))
    print("Shipment-asset links:", len(shipment_assets))
    print("Custody events:", len(custody_events))


if __name__ == "__main__":
    generate_transaction_data()