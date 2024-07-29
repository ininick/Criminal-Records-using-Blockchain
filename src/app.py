from flask import Flask, request, jsonify, render_template
from web3 import Web3
import json

app = Flask(__name__)

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Set default account (use an account from Ganache)
default_account = web3.eth.accounts[0]

# Load contract
with open('../build/contracts/CriminalRecord.json') as f:
    contract_data = json.load(f)
contract_abi = contract_data['abi']
network_id = list(contract_data['networks'].keys())[0]
contract_address = contract_data['networks'][network_id]['address']
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_record', methods=['POST'])
def add_record():
    data = request.get_json()
    
    # Convert age to integer
    age = int(data['age'])
    
    tx_hash = contract.functions.addRecord(
        data['name'],
        age,  # Pass age as an integer
        data['city'],
        data['region'],
        data['crime'],
        data['punishment']
    ).transact({'from': default_account})
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Convert receipt to JSON serializable format
    receipt_dict = {
        'transactionHash': receipt.transactionHash.hex(),
        'transactionIndex': receipt.transactionIndex,
        'blockHash': receipt.blockHash.hex(),
        'blockNumber': receipt.blockNumber,
        'cumulativeGasUsed': receipt.cumulativeGasUsed,
        'gasUsed': receipt.gasUsed,
        'contractAddress': receipt.contractAddress,
        'logs': [dict(log) for log in receipt.logs],
        'status': receipt.status,
    }
    
    return jsonify({'status': 'Record added', 'transaction': receipt_dict})

@app.route('/update_record', methods=['POST'])
def update_record():
    data = request.get_json()
    tx_hash = contract.functions.updateRecord(
        int(data['index']),  # Convert index to integer
        data['name'],
        int(data['age']),  # Ensure age is converted to integer
        data['city'],
        data['region'],
        data['crime'],
        data['punishment']
    ).transact({'from': default_account})
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    # Convert receipt to JSON serializable format
    receipt_dict = {
        'transactionHash': receipt.transactionHash.hex(),
        'transactionIndex': receipt.transactionIndex,
        'blockHash': receipt.blockHash.hex(),
        'blockNumber': receipt.blockNumber,
        'cumulativeGasUsed': receipt.cumulativeGasUsed,
        'gasUsed': receipt.gasUsed,
        'contractAddress': receipt.contractAddress,
        'logs': [dict(log) for log in receipt.logs],
        'status': receipt.status,
    }
    
    return jsonify({'status': 'Record updated', 'transaction': receipt_dict})

@app.route('/get_records', methods=['GET'])
def get_records():
    records = contract.functions.getRecords().call()
    return jsonify(records)

@app.route('/delete_record', methods=['POST'])
def delete_record():
    data = request.get_json()
    record_index = int(data['index'])
    
    tx_hash = contract.functions.deleteRecord(record_index).transact({'from': default_account})
    
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    
    receipt_dict = {
        'transactionHash': receipt.transactionHash.hex(),
        'transactionIndex': receipt.transactionIndex,
        'blockHash': receipt.blockHash.hex(),
        'blockNumber': receipt.blockNumber,
        'cumulativeGasUsed': receipt.cumulativeGasUsed,
        'gasUsed': receipt.gasUsed,
        'contractAddress': receipt.contractAddress,
        'logs': [dict(log) for log in receipt.logs],
        'status': receipt.status,
    }
    
    return jsonify({'status': 'Record deleted', 'transaction': receipt_dict})

if __name__ == '__main__':
    app.run(debug=True)
