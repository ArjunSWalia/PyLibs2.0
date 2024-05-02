import json
from security import SecurityManager

class Transaction:
    def __init__(self, sender, recipient, amount, signature=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "signature": self.signature
        }

    def sign_transaction(self, security_manager, private_key_path):
        security_manager.load_key_from_file(private_key_path, is_private=True)
        transaction_dict = self.to_dict()
        transaction_dict.pop("signature", None)  # Remove the signature field if exists
        transaction_string = json.dumps(transaction_dict, sort_keys=True).encode()
        self.signature = security_manager.sign_data(transaction_string).decode('utf-8')

    @staticmethod
    def verify_transaction(transaction, security_manager):
        """
        Verify the signature of a transaction.
        """
        if transaction["signature"] is None:
            return False
        transaction_copy = transaction.copy()
        signature = transaction_copy.pop("signature")
        transaction_string = json.dumps(transaction_copy, sort_keys=True).encode()
        sender_public_key = security_manager.load_key_from_file(transaction["sender"] + "_public.pem", is_private=False)
        return security_manager.verify_signature(transaction_string, signature.encode('utf-8'), sender_public_key)

class TransactionManager:
    def __init__(self):
        self.transactions = []

    def create_transaction(self, sender, recipient, amount, signature):
        new_transaction = Transaction(sender, recipient, amount, signature)
        self.transactions.append(new_transaction)
        return new_transaction

    def serialize_transactions(self):
        return [tx.to_dict() for tx in self.transactions]

    def add_transaction_from_dict(self, transaction_data):

        new_transaction = Transaction(**transaction_data)
        if Transaction.verify_transaction(new_transaction.to_dict()):
            self.transactions.append(new_transaction)
            return True
        return False

if __name__ == "__main__":
    security_manager = SecurityManager()
    transaction_manager = TransactionManager()

    security_manager.generate_key_pair()  
    security_manager.save_keys_to_file("sender_private_key.pem", "sender_public_key.pem")

    new_transaction = Transaction("sender_address", "recipient_address", 10)
    new_transaction.sign_transaction(security_manager, "sender_private_key.pem")
    print("Signed Transaction:", new_transaction.to_dict())

    added = transaction_manager.add_transaction_from_dict(new_transaction.to_dict())
    print("Transaction added:", added)
