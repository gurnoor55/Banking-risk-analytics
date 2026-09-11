#include "Account.h"
#include <iostream>

using namespace std;

int main() {

    Account account(
        1001,
        "Gurnoor Singh",
        50000
    );

    account.display();

    cout << "\nDepositing 10000...\n";
    account.deposit(10000);

    cout << "Withdrawing 7500...\n";
    account.withdraw(7500);

    cout << "\nUpdated account:\n";
    account.display();

    return 0;
}