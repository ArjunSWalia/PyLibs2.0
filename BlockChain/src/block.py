import hashlib
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0  #mining constant
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()
