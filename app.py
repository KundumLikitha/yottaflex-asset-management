import streamlit as st
import pandas as pd

from database.db import get_connection
from logic.exception_detection import detect_exceptions

st.set_page_config(
    page_title="YottaFlex Asset Management",
    page_icon="📦",
    layout="wide"
)

st.title("YottaFlex Asset Management")
st.subheader("Reusable Asset Tracking Dashboard")

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

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Assets", assets)
col2.metric("Total Shipments", shipments)
col3.metric("Custody Events", custody)
col4.metric("Exceptions", len(exceptions))

st.divider()

st.subheader("Detected Exceptions")

if exceptions:
    exception_df = pd.DataFrame({
        "Exception Details": exceptions
    })
    st.dataframe(exception_df, use_container_width=True)
else:
    st.success("No exceptions detected.")

st.subheader("Project Information")
st.write("Reusable asset tracking across multiple locations.")
st.write("Database: SQLite")
st.write("Dashboard: Streamlit")