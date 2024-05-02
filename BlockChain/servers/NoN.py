from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
node_address = "http://localhost:5000" 
nodes = set() 

@app.route('/register_node', methods=['POST'])
def register_node():
    values = request.get_json()
    nodes.add(values['node'])
    return "Node registered", 200

@app.route('/resolve', methods=['GET'])
def consensus():
    replaced = resolve_conflicts()
    if replaced:
        response = {'message': 'Our chain was replaced'}
    else:
        response = {'message': 'Our chain is authoritative'}
    return jsonify(response), 200

def resolve_conflicts():
    global blockchain
    new_chain = None

    max_length = len(blockchain.chain)

    for node in nodes:
        response = requests.get(f'{node}/chain')

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
