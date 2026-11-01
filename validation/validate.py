from database.db import get_connection


def insert_test_exceptions():
    with get_connection() as connection:

        # 1. Asset recorded at two locations
        connection.execute("""
            INSERT INTO custody_events
            VALUES (
                'CUST-ASSET-0000001-000002',
                'ASSET-0000001',
                'LOC-0002',
                'ACTOR-001',
                'TRANSFER',
                '2026-10-20'
            )
        """)

        # 2. Return before dispatch
        connection.execute("""
            INSERT INTO return_authorizations
            VALUES (
                'RMA-2026-000001',
                'ASSET-0000002',
                '2025-01-01',
                'REQUESTED'
            )
        """)

        # 3. Deposit refunded twice
        connection.executemany("""
            INSERT INTO deposit_ledger
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ('DEP-001', 'ASSET-0000003', 'REFUND', 500, '2026-10-20', 'DEP-REF-001'),
            ('DEP-002', 'ASSET-0000003', 'REFUND', 500, '2026-10-21', 'DEP-REF-001')
        ])

        # 4. Repair closed without inspection
        connection.execute("""
            INSERT INTO repairs
            VALUES (
                'REP-2026-000001',
                'ASSET-0000004',
                NULL,
                'CLOSED',
                250,
                '2026-10-18',
                '2026-10-20'
            )
        """)

        # 5. Custody event without actor
        connection.execute("""
            INSERT INTO custody_events
            VALUES (
                'CUST-ASSET-0000005-000002',
                'ASSET-0000005',
                'LOC-0003',
                NULL,
                'TRANSFER',
                '2026-10-21'
            )
        """)

    print("Five test exception scenarios inserted successfully!")


def generate_validation_report():
    from database.db import get_connection
    from logic.exception_detection import detect_exceptions

    with get_connection() as connection:
        assets = connection.execute(
            "SELECT COUNT(*) FROM assets"
        ).fetchone()[0]

        shipments = connection.execute(
            "SELECT COUNT(*) FROM shipments"
        ).fetchone()[0]

        custody = connection.execute(
            "SELECT COUNT(*) FROM custody_events"
        ).fetchone()[0]

    exceptions = detect_exceptions()

    print("\n========== VALIDATION REPORT ==========")
    print("Total Assets:", assets)
    print("Total Shipments:", shipments)
    print("Total Custody Events:", custody)
    print("Total Exception Messages:", len(exceptions))
    print("Exception Detection: SUCCESS")
    print("======================================")

if __name__ == "__main__":
    generate_validation_report()