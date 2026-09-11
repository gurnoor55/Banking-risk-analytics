#ifndef ACCOUNT_H
#define ACCOUNT_H

#include <string>

class Account {

private:
    int accountID;
    std::string holderName;
    double balance;

public:

    Account(
        int id,
        std::string name,
        double initialBalance
    );

    void deposit(double amount);

    bool withdraw(double amount);

    double getBalance() const;

    void display() const;
};

#endif