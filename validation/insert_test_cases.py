from database.db import get_connection


def insert_test_cases():
    with get_connection() as connection:

        # 1. Same asset at two locations on the same date
        connection.executemany("""
            INSERT INTO custody_events
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("TEST-CUST-001", "ASSET-0000001",
             "LOC-0001", "OWN-0001", "TRANSFER", "2026-10-20"),
            ("TEST-CUST-002", "ASSET-0000001",
             "LOC-0002", "OWN-0001", "TRANSFER", "2026-10-20")
        ])

        # 2. Return before dispatch
        connection.execute("""
            INSERT INTO return_authorizations
            VALUES (?, ?, ?, ?)
        """, (
            "RMA-2026-000001",
            "ASSET-0000002",
            "2025-01-01",
            "REQUESTED"
        ))

        # 3. Duplicate deposit refund
        connection.executemany("""
            INSERT INTO deposit_ledger
            VALUES (?, ?, ?, ?, ?, ?)
        """, [
            ("DEP-001", "ASSET-0000003", "REFUND",
             500, "2026-10-20", "REF-001"),
            ("DEP-002", "ASSET-0000003", "REFUND",
             500, "2026-10-21", "REF-001")
        ])

        # 4. Repair closed without inspection
        connection.execute("""
            INSERT INTO repairs
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "REP-2026-000001",
            "ASSET-0000004",
            None,
            "CLOSED",
            250,
            "2026-10-18",
            "2026-10-20"
        ))

        # 5. Custody event without actor
        connection.execute("""
            INSERT INTO custody_events
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "TEST-CUST-003",
            "ASSET-0000005",
            "LOC-0003",
            None,
            "TRANSFER",
            "2026-10-21"
        ))

    print("Five test scenarios inserted successfully!")


if __name__ == "__main__":
    insert_test_cases()