import hashlib
import time
from urllib.parse import urlparse

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash, self.nonce)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != '0' * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions = []
        self.mining_reward = 1
        self.nodes = set()

    def register_node(self, node_url):
        parsed_url = urlparse(node_url)
        self.nodes.add(parsed_url.netloc)

    def create_genesis_block(self):
        return Block(0, "Genesis Block", time.time(), "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address):
        new_block = Block(index=len(self.chain),
                          transactions=self.pending_transactions,
                          timestamp=time.time(),
                          previous_hash=self.get_last_block().hash)
        new_block.mine_block(self.difficulty)

        print(f"Block successfully mined: {new_block.hash}")
        self.chain.append(new_block)

        self.pending_transactions = [
            {"sender": "network", "recipient": miner_address, "amount": self.mining_reward}
        ]

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                print("Current Hashes not equal")
                return False

            if current.previous_hash != previous.hash:
                print("Previous Hashes not equal")
                return False

        return True

    def resolve_conflicts(self):
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.validate_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False

    def validate_chain(self, chain):
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            current_hash = current_block.calculate_hash()
            if current_hash != current_block['hash']:
                return False

            if current_block['previous_hash'] != previous_block['hash']:
                return False

            if not self.is_valid_proof(current_block, current_block['hash']):
                return False

        return True
