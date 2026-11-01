# Data Dictionary

## 1. asset_types
Stores categories of reusable assets.

## 2. owners
Stores asset owner information.

## 3. locations
Stores warehouses, facilities and other asset locations.

## 4. assets
Stores individual reusable asset details, including asset ID, asset type, owner and status.

## 5. shipments
Stores shipment details, source location, destination location and shipment dates.

## 6. shipment_assets
Links assets to their respective shipments.

## 7. custody_events
Maintains the history of asset movements, locations, actors and event dates.

## 8. return_authorizations
Stores asset return requests and their statuses.

## 9. inspections
Stores inspection information for returned assets.

## 10. repairs
Stores repair details, inspection references, repair status, cost and dates.

## 11. deposit_ledger
Tracks deposits, charges and refunds associated with reusable assets.

## Primary Keys and Relationships

- Each main entity has a unique identifier.
- Shipment assets connect shipments and reusable assets.
- Custody events reference assets and locations.
- Repairs can reference inspections.
- Foreign key constraints help maintain database relationships.

## Notes

The database uses SQLite.
All records are generated as synthetic data for the YottaFlex challenge.