YottaFlex AI – Reusable Asset Management System

Project Overview

An end-to-end reusable asset tracking system designed to monitor the movement, custody, returns, inspections, repairs, and deposits of reusable assets across multiple locations.

Technologies Used

- Python
- SQLite
- Streamlit
- Pandas
- Plotly
- Faker

Key Features

- Reusable asset and master data management
- Shipment and asset movement tracking
- Custody event history
- Return authorization tracking
- Inspection and repair records
- Deposit transaction tracking
- Exception detection and validation
- Interactive Streamlit dashboard
- CSV, JSON, and SQL exports

Dataset

The generated dataset includes:

- 20,000 reusable assets
- 10,000 shipments
- 20,000 shipment-asset links
- 100,000 custody events

Data generation uses a fixed seed: "20261022".

Required Exception Scenarios

1. Asset recorded at two simultaneous locations.
2. Return recorded before dispatch.
3. Deposit refunded twice.
4. Repair closed without inspection.
5. Custody event missing an actor.

All five scenarios have been inserted as test cases and detected by the exception detection logic.

Project Structure

- "app.py" – Streamlit dashboard
- "database/" – Database connection and SQL schema
- "generator/" – Data generation and export scripts
- "logic/" – Asset lifecycle and exception detection
- "validation/" – Validation and test scenarios
- "data/ground_truth/" – Ground-truth test dataset
- "exports/" – CSV, JSON, and SQL exports
- "docs/" – Project documentation
- "prompts/" – AI usage documentation

Setup and Execution

Install dependencies:

pip install -r requirements.txt

Initialize the database:

python -m database.db

Generate master data:

python -m generator.master_data

Generate transaction data:

python -m generator.transaction_data

Generate exports:

python -m generator.export_data

Run the dashboard:

streamlit run app.py

Validation

Run exception detection:

python -m logic.exception_detection

Insert test scenarios:

python -m validation.insert_test_cases

Notes

The project uses synthetic data for demonstration. The exception test cases are deliberately invalid records used to verify detection logic. See the project documentation for implementation details and known limitations.