from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization

class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    def to_json(self):
        return {"sender": self.sender, "recipient": self.recipient, "amount": self.amount}

    def sign_transaction(self, sender_private_key):

        signer = sender_private_key.sign(
            str(self.to_json()).encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        self.signature = signer

    @staticmethod
    def verify_transaction(transaction):
        public_key = serialization.load_pem_public_key(
            transaction.sender.encode(),
            backend=default_backend()
        )
        try:
            public_key.verify(
                transaction.signature,
                str(transaction.to_json()).encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except:
            return False
