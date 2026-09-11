# Banking Transaction Risk Analytics System

A banking transaction analytics system built using **C++, Python, MySQL, and Streamlit**. The project generates synthetic banking data, stores and analyzes it using a relational database, identifies potentially anomalous transactions using statistical risk scoring, and provides an interactive dashboard for data visualization.

---

## Overview

The system simulates a small banking environment containing customers, accounts, and transactions.

The project combines:

- **C++ OOP** for basic banking account operations
- **Python** for data generation, processing, analytics, and anomaly detection
- **MySQL** for structured storage and SQL-based analysis
- **Pandas** for data manipulation
- **Streamlit** for an interactive analytics dashboard
- **Matplotlib** for visualization

The anomaly detection component uses an interpretable statistical approach rather than treating the system as a black-box machine learning model.

---

## Features

- Generate synthetic banking transaction data
- Simulate customer and account information
- Store banking data in a MySQL relational database
- Perform SQL-based transaction and account analytics
- Analyze transaction behaviour using Python and Pandas
- Detect potentially anomalous transactions
- Calculate an interpretable transaction risk score
- Classify transactions into:
  - `NORMAL`
  - `REVIEW`
  - `HIGH`
- Visualize transaction patterns through an interactive dashboard
- Demonstrate object-oriented programming through a C++ banking account module

---

## System Architecture

```text
                 Synthetic Banking Data
                          |
                          v
                +-------------------+
                |  Python Generator |
                +-------------------+
                          |
                          v
                    +----------+
                    |  MySQL   |
                    +----------+
                          |
              +-----------+-----------+
              |                       |
              v                       v
       SQL Analytics          Python Analytics
                                      |
                                      v
                             Anomaly Detection
                                      |
                                      v
                                Risk Scoring
                                      |
                                      v
                            Streamlit Dashboard
