CREATE DATABASE IF NOT EXISTS banking_analytics;

USE banking_analytics;

DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS accounts;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    city VARCHAR(50)
);

CREATE TABLE accounts (
    account_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    account_type VARCHAR(20),
    balance DECIMAL(12,2),
    date_opened DATE,
    
    FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);

CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT NOT NULL,
    transaction_time DATETIME,
    amount DECIMAL(12,2),
    transaction_type VARCHAR(10),
    merchant VARCHAR(100),
    location VARCHAR(50),

    FOREIGN KEY (account_id)
        REFERENCES accounts(account_id)
);

CREATE INDEX idx_transaction_account
ON transactions(account_id);

CREATE INDEX idx_transaction_time
ON transactions(transaction_time);