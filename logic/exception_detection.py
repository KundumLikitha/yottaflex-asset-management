from database.db import get_connection


def detect_exceptions():
    exceptions = []

    with get_connection() as connection:

        # 1. Asset assigned to multiple locations
        query = """
        SELECT asset_id, event_date
        FROM custody_events
        GROUP BY asset_id, event_date
        HAVING COUNT(DISTINCT location_id) > 1
        """

        for row in connection.execute(query):
            exceptions.append(
                f"Asset {row[0]} has multiple recorded locations."
            )

        # 2. Return before dispatch
        query = """
        SELECT r.asset_id, r.requested_date, s.dispatch_date
        FROM return_authorizations r
        JOIN shipment_assets sa ON r.asset_id = sa.asset_id
        JOIN shipments s ON sa.shipment_id = s.shipment_id
        WHERE r.requested_date < s.dispatch_date
        """

        for row in connection.execute(query):
            exceptions.append(
                f"Asset {row[0]} has a return dated before dispatch."
            )

        # 3. Duplicate deposit refunds
        query = """
        SELECT asset_id, reference_id, COUNT(*)
        FROM deposit_ledger
        WHERE transaction_type = 'REFUND'
        GROUP BY asset_id, reference_id
        HAVING COUNT(*) > 1
        """

        for row in connection.execute(query):
            exceptions.append(
                f"Asset {row[0]} has duplicate deposit refunds."
            )

        # 4. Repair closed without inspection
        query = """
        SELECT repair_id
        FROM repairs
        WHERE repair_status = 'CLOSED'
          AND inspection_id IS NULL
        """

        for row in connection.execute(query):
            exceptions.append(
                f"Repair {row[0]} was closed without an inspection."
            )

        # 5. Custody event without actor
        query = """
        SELECT custody_event_id
        FROM custody_events
        WHERE actor_id IS NULL OR TRIM(actor_id) = ''
        """

        for row in connection.execute(query):
            exceptions.append(
                f"Custody event {row[0]} has no actor."
            )

    return exceptions


if __name__ == "__main__":
    results = detect_exceptions()

    print("\nDetected Exceptions:")
    if results:
        for exception in results:
            print("-", exception)
    else:
        print("No exceptions detected.")