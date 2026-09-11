import pandas as pd
import mysql.connector
import random
from datetime import date, timedelta


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

cursor = connection.cursor()

print("Connected to MySQL!")


# =============================
# Read transaction data
# =============================

df = pd.read_csv("data/transactions.csv")

print("Transactions loaded:", len(df))


# =============================
# Generate customers
# =============================

account_ids = sorted(df["account_id"].unique())

random.seed(42)

for account_id in account_ids:

    customer_id = int(account_id)

    name = f"Customer {customer_id}"

    age = random.randint(18, 65)

    city = random.choice([
        "Delhi",
        "Mumbai",
        "Bangalore",
        "Chandigarh",
        "Ludhiana",
        "Pune",
        "Hyderabad"
    ])

    query = """
    INSERT INTO customers
    (customer_id, name, age, city)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            customer_id,
            name,
            age,
            city
        )
    )


# =============================
# Generate accounts
# =============================

for account_id in account_ids:

    account_id = int(account_id)
    customer_id = account_id

    account_type = random.choice([
        "Savings",
        "Current"
    ])

    balance = round(
        random.uniform(
            10000,
            250000
        ),
        2
    )

    date_opened = date(
        2024,
        1,
        1
    ) + timedelta(
        days=random.randint(
            0,
            500
        )
    )

    query = """
    INSERT INTO accounts
    (account_id, customer_id, account_type,
     balance, date_opened)
    VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            account_id,
            customer_id,
            account_type,
            balance,
            date_opened
        )
    )


# =============================
# Insert transactions
# =============================

for _, row in df.iterrows():

    query = """
    INSERT INTO transactions
    (
        transaction_id,
        account_id,
        transaction_time,
        amount,
        transaction_type,
        merchant,
        location
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (
            int(row["transaction_id"]),
            int(row["account_id"]),
            str(row["transaction_time"]),
            float(row["amount"]),
            str(row["transaction_type"]),
            str(row["merchant"]),
            str(row["location"])
        )
    )


# =============================
# Commit changes
# =============================

connection.commit()

cursor.close()
connection.close()

print("All data successfully inserted into MySQL!")