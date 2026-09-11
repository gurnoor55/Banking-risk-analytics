import streamlit as st
import pandas as pd
import mysql.connector


# ==========================================
# Page configuration
# ==========================================

st.set_page_config(
    page_title="Banking Risk Analytics",
    page_icon="🏦",
    layout="wide"
)


# ==========================================
# MySQL configuration
# ==========================================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Your_Password",
    "database": "banking_analytics"
}


# ==========================================
# Database function
# ==========================================

@st.cache_data
def load_data():

    connection = mysql.connector.connect(
        host=DB_CONFIG["host"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"]
    )

    query = """
    SELECT
        transaction_id,
        account_id,
        transaction_time,
        amount,
        transaction_type,
        merchant,
        location
    FROM transactions
    """

    df = pd.read_sql(
        query,
        connection
    )

    connection.close()

    df["transaction_time"] = pd.to_datetime(
        df["transaction_time"]
    )

    return df


# ==========================================
# Load data
# ==========================================

try:

    df = load_data()

except Exception as e:

    st.error(
        f"Database connection failed: {e}"
    )

    st.stop()


# ==========================================
# Title
# ==========================================

st.title(
    "🏦 Banking Risk Analytics"
)

st.write(
    "Transaction monitoring and risk analysis dashboard"
)


# ==========================================
# Sidebar filters
# ==========================================

st.sidebar.header(
    "Filters"
)

locations = sorted(
    df["location"].unique()
)

selected_locations = st.sidebar.multiselect(
    "Location",
    locations,
    default=locations
)

transaction_types = sorted(
    df["transaction_type"].unique()
)

selected_types = st.sidebar.multiselect(
    "Transaction Type",
    transaction_types,
    default=transaction_types
)


# ==========================================
# Apply filters
# ==========================================

filtered_df = df[
    df["location"].isin(selected_locations)
    &
    df["transaction_type"].isin(selected_types)
]


# ==========================================
# KPI cards
# ==========================================

total_transactions = len(
    filtered_df
)

total_value = filtered_df[
    "amount"
].sum()

average_transaction = filtered_df[
    "amount"
].mean()

high_value_transactions = len(
    filtered_df[
        filtered_df["amount"] > 10000
    ]
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Transactions",
    f"{total_transactions:,}"
)

col2.metric(
    "Total Value",
    f"{total_value:,.2f}"
)

col3.metric(
    "Average Transaction",
    f"{average_transaction:,.2f}"
)

col4.metric(
    "High Value",
    f"{high_value_transactions:,}"
)


# ==========================================
# Charts
# ==========================================

st.divider()

col1, col2 = st.columns(2)


# Transaction type

with col1:

    st.subheader(
        "Transactions by Type"
    )

    type_data = (
        filtered_df[
            "transaction_type"
        ]
        .value_counts()
    )

    st.bar_chart(
        type_data
    )


# Location

with col2:

    st.subheader(
        "Transactions by Location"
    )

    location_data = (
        filtered_df[
            "location"
        ]
        .value_counts()
    )

    st.bar_chart(
        location_data
    )


# ==========================================
# Merchant analysis
# ==========================================

st.divider()

st.subheader(
    "Top Merchants"
)

merchant_data = (
    filtered_df
    .groupby("merchant")["amount"]
    .sum()
    .sort_values(
        ascending=False
    )
    .head(10)
)

st.bar_chart(
    merchant_data
)


# ==========================================
# High-value transactions
# ==========================================

st.divider()

st.subheader(
    "Highest-Value Transactions"
)

high_value = (
    filtered_df
    .nlargest(
        20,
        "amount"
    )
)

st.dataframe(
    high_value[
        [
            "transaction_id",
            "account_id",
            "transaction_time",
            "amount",
            "transaction_type",
            "merchant",
            "location"
        ]
    ],
    use_container_width=True
)


# ==========================================
# Summary
# ==========================================

st.divider()

st.subheader(
    "Dataset Summary"
)

st.write(
    f"Showing {len(filtered_df):,} "
    f"transactions after applying filters."
)