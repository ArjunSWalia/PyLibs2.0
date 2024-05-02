import json
from decimal import Decimal
from transaction_manager import TransactionManager, Transaction
from security import SecurityManager

class Cryptocurrency:
    def __init__(self, name="WaliaCoin", symbol="WC", initial_supply=1000000, transaction_manager=None):
        self.name = name
        self.symbol = symbol
        self.initial_supply = initial_supply
        self.transaction_manager = transaction_manager or TransactionManager()
        self.security_manager = SecurityManager()
        self.ledger = [Transaction("genesis", "foundation_wallet", initial_supply).to_dict()]

    def calculate_balance(self, address):
        balance = Decimal(0)
        for transaction in self.ledger + self.transaction_manager.transactions:
            if transaction.sender == address:
                balance -= Decimal(transaction.amount)
            if transaction.recipient == address:
                balance += Decimal(transaction.amount)
        return balance

    def create_transaction(self, sender, recipient, amount, private_key_path):
        if self.calculate_balance(sender) < Decimal(amount):
            raise ValueError("Insufficient balance to complete this transaction.")
        new_transaction = Transaction(sender, recipient, amount)
        new_transaction.sign_transaction(self.security_manager, private_key_path)
        if Transaction.verify_transaction(new_transaction.to_dict(), self.security_manager):
            self.transaction_manager.add_transaction_from_dict(new_transaction.to_dict())
            self.ledger.append(new_transaction.to_dict())
            return True
        return False

    def issue_reward(self, miner_address, reward_amount):
        reward_transaction = Transaction("network", miner_address, reward_amount).to_dict()
        self.ledger.append(reward_transaction)
        print(f"Issued {reward_amount} {self.symbol} to {miner_address} as mining reward.")

    def process_transactions(self):
        for transaction in self.transaction_manager.transactions:
            if Transaction.verify_transaction(transaction.to_dict(), self.security_manager):
                self.ledger.append(transaction.to_dict())
        self.transaction_manager.transactions = []  

if __name__ == "__main__":
    crypto = Cryptocurrency()
    crypto.issue_reward("miner_wallet", 50)  

    sender_private_key_path = "" #TODO: create .pem file
    try:
        crypto.create_transaction("foundation_wallet", "user_wallet", 100, sender_private_key_path)
        print("Transaction successfully created and added to the ledger.")
    except ValueError as e:
        print(e)

    balance = crypto.calculate_balance("user_wallet")
    print(f"User wallet balance: {balance} {crypto.symbol}")
