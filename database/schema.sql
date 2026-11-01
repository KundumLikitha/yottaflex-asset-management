PRAGMA foreign_keys = ON;

-- 1. Asset types
CREATE TABLE IF NOT EXISTS asset_types (
    asset_type_id TEXT PRIMARY KEY,
    type_name TEXT NOT NULL UNIQUE,
    description TEXT
);

-- 2. Owners
CREATE TABLE IF NOT EXISTS owners (
    owner_id TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL,
    owner_type TEXT NOT NULL
        CHECK (owner_type IN ('COMPANY', 'SUPPLIER', 'CUSTOMER'))
);

-- 3. Locations
CREATE TABLE IF NOT EXISTS locations (
    location_id TEXT PRIMARY KEY,
    location_name TEXT NOT NULL,
    city TEXT,
    country TEXT
);

-- 4. Reusable assets
CREATE TABLE IF NOT EXISTS assets (
    asset_id TEXT PRIMARY KEY,
    asset_type_id TEXT NOT NULL,
    owner_id TEXT NOT NULL,
    serial_number TEXT UNIQUE NOT NULL,
    current_status TEXT NOT NULL DEFAULT 'AVAILABLE'
        CHECK (current_status IN (
            'AVAILABLE', 'IN_TRANSIT', 'WITH_SUPPLIER',
            'RETURNED', 'DAMAGED', 'UNDER_REPAIR', 'LOST',
            'RETIRED'
        )),
    created_at TEXT NOT NULL,
    FOREIGN KEY (asset_type_id) REFERENCES asset_types(asset_type_id),
    FOREIGN KEY (owner_id) REFERENCES owners(owner_id)
);

-- 5. Shipments
CREATE TABLE IF NOT EXISTS shipments (
    shipment_id TEXT PRIMARY KEY,
    source_location_id TEXT NOT NULL,
    destination_location_id TEXT NOT NULL,
    dispatch_date TEXT NOT NULL,
    expected_return_date TEXT,
    shipment_status TEXT NOT NULL,
    FOREIGN KEY (source_location_id) REFERENCES locations(location_id),
    FOREIGN KEY (destination_location_id) REFERENCES locations(location_id)
);

-- 6. Shipment and asset relationship
CREATE TABLE IF NOT EXISTS shipment_assets (
    shipment_id TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    PRIMARY KEY (shipment_id, asset_id),
    FOREIGN KEY (shipment_id) REFERENCES shipments(shipment_id),
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- 7. Custody history
CREATE TABLE IF NOT EXISTS custody_events (
    custody_event_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    actor_id TEXT,
    event_type TEXT NOT NULL,
    event_date TEXT NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

-- 8. Return authorizations
CREATE TABLE IF NOT EXISTS return_authorizations (
    rma_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    requested_date TEXT NOT NULL,
    return_status TEXT NOT NULL,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- 9. Inspections
CREATE TABLE IF NOT EXISTS inspections (
    inspection_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    inspection_date TEXT NOT NULL,
    inspection_result TEXT NOT NULL
        CHECK (inspection_result IN ('GOOD', 'DAMAGED', 'BEYOND_REPAIR')),
    notes TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- 10. Repairs
CREATE TABLE IF NOT EXISTS repairs (
    repair_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    inspection_id TEXT,
    repair_status TEXT NOT NULL,
    repair_cost REAL DEFAULT 0 CHECK (repair_cost >= 0),
    opened_date TEXT NOT NULL,
    closed_date TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    FOREIGN KEY (inspection_id) REFERENCES inspections(inspection_id)
);

-- 11. Deposit ledger
CREATE TABLE IF NOT EXISTS deposit_ledger (
    transaction_id TEXT PRIMARY KEY,
    asset_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL
        CHECK (transaction_type IN ('CHARGE', 'REFUND')),
    amount REAL NOT NULL CHECK (amount > 0),
    transaction_date TEXT NOT NULL,
    reference_id TEXT,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_assets_status
ON assets(current_status);

CREATE INDEX IF NOT EXISTS idx_custody_asset
ON custody_events(asset_id);

CREATE INDEX IF NOT EXISTS idx_shipments_date
ON shipments(dispatch_date);

CREATE INDEX IF NOT EXISTS idx_returns_asset
ON return_authorizations(asset_id);