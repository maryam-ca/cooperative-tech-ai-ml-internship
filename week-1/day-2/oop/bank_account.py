"""
Digital Wallet System
"""

class DigitalWallet:

    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.balance = 0
        self.transactions = []

    def deposit(self, amount):
        self.balance += amount
        self.transactions.append(f"Deposited {amount}")

    def withdraw(self, amount):

        if amount > self.balance:
            print("Insufficient Balance")
            return

        self.balance -= amount
        self.transactions.append(f"Withdrawn {amount}")

    def show_balance(self):
        print("\nCurrent Balance:", self.balance)

    def show_transactions(self):
        print("\nTransaction History")

        for transaction in self.transactions:
            print(transaction)


wallet = DigitalWallet("Maryam")

wallet.deposit(5000)
wallet.deposit(3000)
wallet.withdraw(2000)

wallet.show_balance()
wallet.show_transactions()