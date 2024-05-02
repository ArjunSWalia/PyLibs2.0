import requests

class NetworkManager:
    def __init__(self, blockchain, node_address):
        self.blockchain = blockchain
        self.nodes = set()
        self.node_address = node_address

    def register_node(self, address):
        self.nodes.add(address)

    def unregister_node(self, address):
        self.nodes.discard(address)

    def broadcast_transaction(self, transaction):
        for node in self.nodes:
            try:
                requests.post(f'http://{node}/transactions/new', json=transaction, timeout=2)
            except requests.exceptions.RequestException:
                print(f"Node {node} is not reachable.")

    def broadcast_new_block(self, block):
        for node in self.nodes:
            try:
                requests.post(f'http://{node}/block/new', json={"block": block}, timeout=2)
            except requests.exceptions.RequestException:
                print(f"Node {node} is not reachable.")

    def resolve_conflicts(self):
        longest_chain = None
        max_length = len(self.blockchain.chain)

        for node in self.nodes:
            try:
                response = requests.get(f'http://{node}/chain', timeout=2)

                if response.status_code == 200:
                    length = response.json()['length']
                    chain = response.json()['chain']

                    if length > max_length and self.blockchain.validate_chain(chain):
                        max_length = length
                        longest_chain = chain
            except requests.exceptions.RequestException:
                continue

        if longest_chain:
            self.blockchain.chain = longest_chain
            return True

        return False

if __name__ == "__main__":
    from blockchain import Blockchain  
    blockchain = Blockchain()
    node_address = "localhost:5000"
    network_manager = NetworkManager(blockchain, node_address)
    network_manager.register_node("localhost:5001")  
    print("Nodes in the network:", network_manager.nodes)
