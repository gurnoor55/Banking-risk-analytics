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
# Load transactions
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
# Account statistics
# =============================

account_mean = (
    df.groupby("account_id")["amount"]
    .transform("mean")
)

account_std = (
    df.groupby("account_id")["amount"]
    .transform("std")
    .fillna(0)
)

df["z_score"] = (
    (df["amount"] - account_mean)
    / account_std.replace(0, 1)
)


# =============================
# Transaction frequency
# =============================

account_frequency = (
    df.groupby("account_id")["transaction_id"]
    .transform("count")
)

df["account_frequency"] = account_frequency


# =============================
# Risk scoring
# =============================

df["risk_score"] = 0


# Rule 1:
# Unusually large compared with
# the account's normal behaviour

df.loc[
    df["z_score"] > 2,
    "risk_score"
] += 40


# Rule 2:
# Extremely unusual transaction

df.loc[
    df["z_score"] > 3,
    "risk_score"
] += 30


# Rule 3:
# Very large transaction

df.loc[
    df["amount"] > 10000,
    "risk_score"
] += 20


# Rule 4:
# Extremely high transaction frequency

frequency_limit = (
    df["account_frequency"].mean()
    + 2 * df["account_frequency"].std()
)

df.loc[
    df["account_frequency"] > frequency_limit,
    "risk_score"
] += 10


# Make sure score never exceeds 100

df["risk_score"] = df["risk_score"].clip(
    upper=100
)


# =============================
# Risk classification
# =============================

df["risk"] = "NORMAL"

df.loc[
    df["risk_score"] >= 40,
    "risk"
] = "REVIEW"

df.loc[
    df["risk_score"] >= 70,
    "risk"
] = "HIGH"


# =============================
# Display results
# =============================

print("\n===== RISK ANALYSIS =====")

print(
    df["risk"]
    .value_counts()
)


print("\nRisk score summary:")

print(
    df["risk_score"]
    .describe()
)


print("\nHighest-risk transactions:")

high_risk = (
    df.sort_values(
        "risk_score",
        ascending=False
    )
    .head(20)
)

print(
    high_risk[
        [
            "transaction_id",
            "account_id",
            "amount",
            "merchant",
            "location",
            "z_score",
            "risk_score",
            "risk"
        ]
    ].to_string(index=False)
)


# =============================
# Save results
# =============================

df.to_csv(
    "data/analyzed_transactions.csv",
    index=False
)


# =============================
# Close connection
# =============================

connection.close()

print("\nRisk analysis completed!")
print("Results saved to data/analyzed_transactions.csv")