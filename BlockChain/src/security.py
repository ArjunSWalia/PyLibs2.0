import os
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import constant_time
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

class SecurityManager:
    def __init__(self):
        self.private_key = None
        self.public_key = None

    def generate_key_pair(self, key_size=2048):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())
        self.public_key = self.private_key.public_key()

    def save_keys_to_file(self, private_key_path="private_key.pem", public_key_path="public_key.pem"):
        private_pem = self.private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                     format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                     encryption_algorithm=serialization.NoEncryption())

        public_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PublicFormat.SubjectPublicKeyInfo)

        with open(private_key_path, "wb") as priv_file:
            priv_file.write(private_pem)

        with open(public_key_path, "wb") as pub_file:
            pub_file.write(public_pem)

    def load_key_from_file(self, file_path, is_private=True):
        with open(file_path, "rb") as key_file:
            if is_private:
                self.private_key = serialization.load_pem_private_key(key_file.read(), password=None, backend=default_backend())
            else:
                self.public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

    def sign_data(self, data):
        if not self.private_key:
            raise ValueError("Private key not loaded.")
        signer = self.private_key.sign(data, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                         salt_length=padding.PSS.MAX_LENGTH),
                                       hashes.SHA256())
        return base64.b64encode(signer)

    def verify_signature(self, data, signature, public_key=None):
        if public_key is None:
            public_key = self.public_key
        try:
            public_key.verify(base64.b64decode(signature), data,
                              padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                          salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
            return True
        except InvalidSignature:
            return False

    def encrypt_message(self, message, symmetric_key):
        fernet = Fernet(symmetric_key)
        return fernet.encrypt(message.encode())

    def decrypt_message(self, encrypted_message, symmetric_key):
        fernet = Fernet(symmetric_key)
        return fernet.decrypt(encrypted_message).decode()

    @staticmethod
    def generate_symmetric_key(password_provided, salt=os.urandom(16)):
        password = password_provided.encode()   
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                         iterations=100000, backend=default_backend())
        key = base64.urlsafe_b64encode(kdf.derive(password)) 
        return key, salt

    @staticmethod
    def hash_data(data):
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data.encode())
        return digest.finalize().hex()

if __name__ == "__main__":
    security_manager = SecurityManager()
    security_manager.generate_key_pair()
    security_manager.save_keys_to_file()
    security_manager.load_key_from_file("private_key.pem", is_private=True)

    data = "Blockchain data"
    signature = security_manager.sign_data(data.encode())
    print("Signature:", signature)

    verification = security_manager.verify_signature(data.encode(), signature)
    print("Verification:", verification)

    symmetric_key, salt = SecurityManager.generate_symmetric_key("password123")
    encrypted_message = security_manager.encrypt_message("Hello, Blockchain!", symmetric_key)
    print("Encrypted:", encrypted_message)

    decrypted_message = security_manager.decrypt_message(encrypted_message, symmetric_key)
    print("Decrypted:", decrypted_message)
