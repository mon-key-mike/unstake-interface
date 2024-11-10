from web3 import Web3
import getpass

# Connect to the Sepolia Ethereum test network
sepolia_url = "https://sepolia.infura.io/v3/7d82b7d35b364974b396cf4e87900165"
web3 = Web3(Web3.HTTPProvider(sepolia_url))

# Check if connected
if not web3.is_connected():
    print("Unable to connect to Ethereum network.")
    exit()

# Get user inputs
wallet_address = input("Enter your wallet address: ")
private_key = getpass.getpass("Enter your private key (hidden input): ")
receiver_address = input("Enter the receiver's wallet address: ")
amount_in_eth = float(input("Enter the amount of ETH to send (e.g., 0.001): "))

# Convert receiver address to checksum format
receiver_address = Web3.to_checksum_address(receiver_address)

# Build the transaction
transaction = {
    'from': wallet_address,
    'to': receiver_address,
    'value': web3.to_wei(amount_in_eth, 'ether'),
    'gas': 21000,
    'gas_price': web3.eth.gas_price,
    'nonce': web3.eth.get_transaction_count(wallet_address),
    'chainId': 11155111  # Chain ID for Sepolia test network
}

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Display transaction hash
print(f"Transaction sent! You can view it at https://sepolia.etherscan.io/tx/{web3.to_hex(tx_hash)}")
