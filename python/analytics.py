import pandas as pd
import mysql.connector


# =============================
# MySQL configuration
# =============================

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "YOUR_PASSWORD",
    "database": "banking_analytics"
}


# =============================
# Connect to MySQL
# =============================

connection = mysql.connector.connect(
    host=DB_CONFIG["host"],
    user=DB_CONFIG["user"],
    password=DB_CONFIG["password"],
    database=DB_CONFIG["database"]
)

print("Connected to MySQL!")


# =============================
# Load transactions from MySQL
# =============================

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

df = pd.read_sql(query, connection)

print("Transactions loaded:", len(df))


# =============================
# Basic Analytics
# =============================

print("\n===== TRANSACTION ANALYTICS =====")


print("\nTotal transactions:")

print(
    len(df)
)


print("\nTotal transaction value:")

print(
    df["amount"].sum()
)


print("\nAverage transaction:")

print(
    df["amount"].mean()
)


# =============================
# Transaction type analysis
# =============================

print("\nTransactions by type:")

print(
    df["transaction_type"].value_counts()
)


# =============================
# Merchant analysis
# =============================

print("\nTop merchants:")

print(
    df["merchant"]
    .value_counts()
    .head(10)
)


# =============================
# Location analysis
# =============================

print("\nTransactions by location:")

print(
    df["location"]
    .value_counts()
)


# =============================
# Highest-value transactions
# =============================

print("\nHighest-value transactions:")

print(
    df.nlargest(
        10,
        "amount"
    )[
        [
            "transaction_id",
            "account_id",
            "amount",
            "merchant",
            "location"
        ]
    ].to_string(index=False)
)

# =============================
# SQL-based analytics
# =============================

print("\n===== SQL ANALYTICS =====")


# Total value by transaction type

query = """
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_amount
FROM transactions
GROUP BY transaction_type
"""

result = pd.read_sql(
    query,
    connection
)

print("\nTransaction summary:")

print(
    result.to_string(index=False)
)


# =============================
# Top accounts
# =============================

query = """
SELECT
    account_id,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount), 2) AS total_value
FROM transactions
GROUP BY account_id
ORDER BY total_value DESC
LIMIT 10
"""

result = pd.read_sql(
    query,
    connection
)

print("\nTop 10 accounts by transaction value:")

print(
    result.to_string(index=False)
)

query = """
SELECT
    c.customer_id,
    c.name,
    c.city,
    a.account_id,
    a.account_type,
    a.balance
FROM customers c

JOIN accounts a
    ON c.customer_id = a.customer_id

ORDER BY a.balance DESC
LIMIT 10
"""

result = pd.read_sql(
    query,
    connection
)

print("\nTop 10 accounts by balance:")

print(
    result.to_string(index=False)
)

# =============================
# Close connection
# =============================

connection.close()

print("\nConnection closed.")