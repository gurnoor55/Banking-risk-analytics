import pandas as pd
import matplotlib.pyplot as plt
import os


# =============================
# Paths
# =============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

DASHBOARD_DIR = os.path.join(
    BASE_DIR,
    "dashboard"
)

os.makedirs(
    DASHBOARD_DIR,
    exist_ok=True
)


# =============================
# Load analysed data
# =============================

df = pd.read_csv(
    os.path.join(
        DATA_DIR,
        "analyzed_transactions.csv"
    )
)

df["transaction_time"] = pd.to_datetime(
    df["transaction_time"]
)


# =============================
# 1. Monthly transaction value
# =============================

monthly = (
    df.set_index("transaction_time")
    .resample("ME")["amount"]
    .sum()
)

plt.figure(figsize=(9, 5))

monthly.plot()

plt.title(
    "Monthly Transaction Value"
)

plt.xlabel("Month")

plt.ylabel(
    "Transaction Value"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        DASHBOARD_DIR,
        "monthly_transaction_value.png"
    )
)

plt.close()


# =============================
# 2. Risk distribution
# =============================

risk_counts = (
    df["risk"]
    .value_counts()
)

plt.figure(figsize=(7, 5))

risk_counts.plot(
    kind="bar"
)

plt.title(
    "Transaction Risk Distribution"
)

plt.xlabel(
    "Risk Level"
)

plt.ylabel(
    "Number of Transactions"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        DASHBOARD_DIR,
        "risk_distribution.png"
    )
)

plt.close()


# =============================
# 3. Top merchants
# =============================

merchant_counts = (
    df["merchant"]
    .value_counts()
    .head(10)
)

plt.figure(figsize=(9, 5))

merchant_counts.plot(
    kind="bar"
)

plt.title(
    "Top Merchants by Transaction Count"
)

plt.xlabel(
    "Merchant"
)

plt.ylabel(
    "Transactions"
)

plt.xticks(
    rotation=45,
    ha="right"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        DASHBOARD_DIR,
        "top_merchants.png"
    )
)

plt.close()


# =============================
# 4. Risk score distribution
# =============================

plt.figure(figsize=(9, 5))

df["risk_score"].plot(
    kind="hist",
    bins=20
)

plt.title(
    "Risk Score Distribution"
)

plt.xlabel(
    "Risk Score"
)

plt.ylabel(
    "Number of Transactions"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        DASHBOARD_DIR,
        "risk_score_distribution.png"
    )
)

plt.close()


print("Dashboard generated successfully!")

print("\nFiles created:")

print("monthly_transaction_value.png")
print("risk_distribution.png")
print("top_merchants.png")
print("risk_score_distribution.png")