def consensus(blockchain, network_nodes):
    new_chain = None
    max_length = len(blockchain.chain)

    for node_address in network_nodes:
        response = requests.get(f'http://{node_address}/chain')
        if response.status_code == 200:
            length = response.json()['length']
            chain = response.json()['chain']

            if length > max_length and blockchain.validate_chain(chain):
                max_length = length
                new_chain = chain

    if new_chain:
        blockchain.chain = new_chain
        return True

    return False
