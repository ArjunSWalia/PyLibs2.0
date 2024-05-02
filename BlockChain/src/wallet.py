import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

class Wallet:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
        self.public_key = self.private_key.public_key()

    def save_keys(self):
        if self.private_key is not None and self.public_key is not None:
            private_pem = self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                         format=serialization.PrivateFormat.PKCS8,
                                                         encryption_algorithm=serialization.NoEncryption())

            public_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)

            with open("private_key.pem", "wb") as priv_file:
                priv_file.write(private_pem)

            with open("public_key.pem", "wb") as pub_file:
                pub_file.write(public_pem)

    def load_keys(self):
        try:
            with open("private_key.pem", "rb") as priv_file:
                self.private_key = serialization.load_pem_private_key(priv_file.read(), password=None, backend=default_backend())

            with open("public_key.pem", "rb") as pub_file:
                self.public_key = serialization.load_pem_public_key(pub_file.read(), backend=default_backend())

        except FileNotFoundError:
            print("No wallet found. Generating a new one...")
            self.generate_keys()
            self.save_keys()

    def sign_transaction(self, sender, recipient, amount):
        signer = self.private_key.sign(
            f"{sender}{recipient}{amount}".encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return signer.hex()

    def get_public_key(self):
        return self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                            format=serialization.PublicFormat.SubjectPublicKeyInfo).decode("utf-8")

if __name__ == "__main__":
    wallet = Wallet()
    wallet.load_keys()
    print("Public Key:", wallet.get_public_key())
