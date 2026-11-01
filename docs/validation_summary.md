# Validation Summary

## Dataset Overview

| Entity | Records |
|---|---:|
| Assets | 20,000 |
| Shipments | 10,000 |
| Custody Events | 100,003 |
| Return Authorizations | 1 |
| Inspections | 0 |
| Repairs | 1 |
| Deposit Ledger | 2 |

## Validation Results

| Check | Result |
|---|---|
| Asset primary key uniqueness | PASS |
| Foreign key relationships | PASS |
| Required asset IDs | PASS |
| Custody event date validity | PASS |

## Exception Detection

Five required exception scenarios were tested:

1. Asset recorded at two locations.
2. Return before dispatch.
3. Deposit refunded twice.
4. Repair closed without inspection.
5. Custody event missing actor.

All five scenarios were detected successfully.

## Conclusion

The current database passed all implemented validation checks.
All five required exception scenarios were detected successfully.

Note: Inspection records are currently empty.