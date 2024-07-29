from web3 import Web3
import json

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

# Add default account as validator
tx_hash = contract.functions.addValidator(default_account).transact({'from': default_account})
receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f"Default account {default_account} added as validator with transaction {receipt.transactionHash.hex()}")

# Dummy data
dummy_records = [
    {"name": "John Doe", "age": 30, "city": "New York", "region": "NY", "crime": "Theft", "punishment": "2 years"},
    {"name": "Jane Smith", "age": 25, "city": "Los Angeles", "region": "CA", "crime": "Fraud", "punishment": "3 years"},
    {"name": "Alice Johnson", "age": 35, "city": "Chicago", "region": "IL", "crime": "Robbery", "punishment": "5 years"}
]

# Add dummy data to blockchain
for record in dummy_records:
    tx_hash = contract.functions.addRecord(
        record['name'],
        record['age'],
        record['city'],
        record['region'],
        record['crime'],
        record['punishment']
    ).transact({'from': default_account})
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Added record: {record['name']} with transaction {receipt.transactionHash.hex()}")
