import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

# ==========================================
# Configuration
# ==========================================

NUM_ACCOUNTS = 100
NUM_TRANSACTIONS = 10000
ANOMALY_COUNT = 100

cities = [
    "Delhi",
    "Mumbai",
    "Bangalore",
    "Chandigarh",
    "Ludhiana",
    "Pune",
    "Hyderabad"
]

merchants = [
    "Amazon",
    "Walmart",
    "Uber",
    "Netflix",
    "Apple",
    "Flipkart",
    "Swiggy",
    "Myntra",
    "Shell",
    "Local Store"
]

# ==========================================
# Generate transactions
# ==========================================

transactions = []

start_date = datetime(2026, 1, 1)

for i in range(1, NUM_TRANSACTIONS + 1):

    account_id = random.randint(
        1,
        NUM_ACCOUNTS
    )

    # Each account has its own spending behaviour
    base_amount = random.uniform(
        500,
        5000
    )

    amount = random.gauss(
        base_amount,
        base_amount * 0.25
    )

    amount = max(
        50,
        round(amount, 2)
    )

    transaction_type = random.choices(
        ["DEBIT", "CREDIT"],
        weights=[0.75, 0.25]
    )[0]

    transaction_time = (
        start_date
        + timedelta(
            minutes=random.randint(
                0,
                300000
            )
        )
    )

    merchant = random.choice(
        merchants
    )

    location = random.choice(
        cities
    )

    transactions.append([
        i,
        account_id,
        transaction_time,
        amount,
        transaction_type,
        merchant,
        location,
        False
    ])


# ==========================================
# Inject anomalous transactions
# ==========================================

for i in range(
    ANOMALY_COUNT
):

    transaction_index = random.randint(
        0,
        NUM_TRANSACTIONS - 1
    )

    account_id = transactions[
        transaction_index
    ][1]

    # Extremely large transaction
    amount = round(
        random.uniform(
            30000,
            75000
        ),
        2
    )

    transaction_time = (
        start_date
        + timedelta(
            minutes=random.randint(
                0,
                300000
            )
        )
    )

    merchant = random.choice(
        merchants
    )

    location = random.choice(
        cities
    )

    transactions[
        transaction_index
    ] = [
        transactions[
            transaction_index
        ][0],
        account_id,
        transaction_time,
        amount,
        "DEBIT",
        merchant,
        location,
        True
    ]


# ==========================================
# Create DataFrame
# ==========================================

df = pd.DataFrame(
    transactions,
    columns=[
        "transaction_id",
        "account_id",
        "transaction_time",
        "amount",
        "transaction_type",
        "merchant",
        "location",
        "known_anomaly"
    ]
)


# ==========================================
# Save dataset
# ==========================================

df.to_csv(
    "data/transactions.csv",
    index=False
)

print("================================")
print("Banking dataset generated")
print("================================")

print(
    "Transactions:",
    len(df)
)

print(
    "Accounts:",
    df["account_id"].nunique()
)

print(
    "Known anomalies:",
    df["known_anomaly"].sum()
)

print(
    "Average transaction:",
    round(
        df["amount"].mean(),
        2
    )
)

print("\nData saved to:")
print("data/transactions.csv")