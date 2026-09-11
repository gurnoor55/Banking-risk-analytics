#include "Account.h"
#include <iostream>

using namespace std;

Account::Account(
    int id,
    string name,
    double initialBalance
) {
    accountID = id;
    holderName = name;
    balance = initialBalance;
}

void Account::deposit(double amount) {

    if (amount > 0)
        balance += amount;
}

bool Account::withdraw(double amount) {

    if (amount <= 0 || amount > balance)
        return false;

    balance -= amount;
    return true;
}

double Account::getBalance() const {
    return balance;
}

void Account::display() const {

    cout << "Account ID: "
         << accountID << endl;

    cout << "Holder: "
         << holderName << endl;

    cout << "Balance: "
         << balance << endl;
}