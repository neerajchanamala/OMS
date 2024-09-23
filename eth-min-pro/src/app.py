from flask import Flask, render_template, request, redirect
from web3 import Web3, HTTPProvider
import json

blockchain = "http://127.0.0.1:7545"  # Default Ganache URL
web3 = Web3(HTTPProvider(blockchain))
web3.eth.defaultAccount = web3.eth.accounts[1]

artifact = "../build/contracts/LandRegistry.json"
with open(artifact) as f:
    artifact_json = json.load(f)
    contract_abi = artifact_json['abi']
    contract_address = artifact_json['networks']['5777']['address']
contract = web3.eth.contract(
    abi=contract_abi,
    address=contract_address
)

app = Flask(__name__)

# Store properties in memory (could be a database in production)
properties = []

@app.route('/')
def home():
    return render_template('index.html', properties=properties)

@app.route('/register', methods=['GET', 'POST'])
def register_property():
    owner_name = request.form.get('ownerName')
    property_address = request.form.get('propertyAddress')
    description = request.form.get('description')
    price = request.form.get('price')

    # Call the smart contract function to register the property
    tx_hash = contract.functions.registerProperty(property_address, int(price)).transact({
        'from': web3.eth.defaultAccount  # Specify the sender's address
    })

    # Wait for the transaction to be mined
    web3.eth.wait_for_transaction_receipt(tx_hash)

    # Create a new property dictionary and append it to the list
    new_property = {
        'ownerName': owner_name,  # You can keep ownerName here for the frontend
        'propertyAddress': property_address,
        'description': description,
        'price': price
    }
    properties.append(new_property)

    # Redirect to the home page
    return redirect('/')



@app.route('/transfer', methods=['GET', 'POST'])
def transfer_ownership():
    property_id = int(request.form.get('propertyId'))
    new_owner_name = request.form.get('newOwnerName')
    new_owner_address = request.form.get('newOwnerAddress')

    # Check if the property ID is valid
    if 0 < property_id <= len(properties):
        # Update the in-memory properties list
        properties[property_id - 1]['ownerName'] = new_owner_name
        properties[property_id - 1]['propertyAddress'] = new_owner_address

        # Call the smart contract function to transfer ownership
        tx_hash = contract.functions.transferOwnership(property_id, new_owner_address).transact({
            'from': web3.eth.defaultAccount  # Ensure this is set before
        })

        # Wait for the transaction to be mined
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        # Print transaction details (optional)
        print("Transaction Hash:", receipt.transactionHash.hex())
        print("Block Number:", receipt.blockNumber)
        print("Gas Used:", receipt.gasUsed)

        # Access event logs from the receipt
        event_logs = []
        for log in receipt.logs:
            try:
                # Decode log using the contract's event signature
                event = contract.events.YourEventName().processReceipt(receipt)
                event_logs.append(event)
                print("Event:", event)
            except Exception as e:
                print(f"Error processing log: {e}")

    else:
        return "Property ID is invalid", 400  # Return error for invalid ID

    # Optionally return transaction details to the front end
    return redirect('/')



if __name__ == '__main__':
    app.run(debug=True)
