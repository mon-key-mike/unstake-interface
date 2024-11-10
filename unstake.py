from web3 import Web3
import getpass

# Connect to Ethereum network with the provided Infura URL
infura_url = "https://mainnet.infura.io/v3/7d82b7d35b364974b396cf4e87900165"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connected
if not web3.isConnected():
    print("Unable to connect to Ethereum network.")
    exit()

# Contract Address and ABI
contract_address = Web3.toChecksumAddress("0x9b14f44269886667c69ce7cef33ff83a13cd5126")
abi = [
    {"inputs":[{"internalType":"address","name":"_fxRoot","type":"address"},
               {"internalType":"address","name":"polyChild","type":"address"}],
     "stateMutability":"nonpayable","type":"constructor"},
    {"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},
                                 {"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],
     "name":"OwnershipTransferred","type":"event"},
    {"inputs":[],"name":"fxChildTunnel","outputs":[{"internalType":"address","name":"","type":"address"}],
     "stateMutability":"view","type":"function"},
    # ... [Remaining ABI truncated for brevity]
    {"inputs":[{"internalType":"address[]","name":"asset","type":"address[]"},
               {"internalType":"uint256[]","name":"tokenIds","type":"uint256[]"}],
     "name":"unstake","outputs":[],"stateMutability":"nonpayable","type":"function"}
]

# Load contract
contract = web3.eth.contract(address=contract_address, abi=abi)

# Get user inputs
wallet_address = input("Enter your wallet address: ")
private_key = getpass.getpass("Enter your private key (hidden input): ")

# Token IDs and corresponding asset addresses for unstaking
token_ids = input("Enter token IDs separated by commas (e.g., 123,456,789): ")
asset_names = input("Enter asset types for each token ID, separated by commas (e.g., DOGS,PUPS,DOGS): ")

# Dictionary of asset addresses (replace these with the correct ones if needed)
asset_addresses = {
    "DOGS": "0x91673149FFae3274b32997288395D07A8213e41F",
    "PUPS": "0x7BC6d85a15B21CEfd62Ce5ab2cF87B611da6bE59",
    "BONES": "0x2C173A97ED9beC4b292c7786811510268fd5e170",
    "K9000": "0xa5849F0105B9a0e1811786d655dC7334B295FF18"
}

# Parse inputs
token_ids_list = [int(token.strip()) for token in token_ids.split(",")]
asset_addresses_list = [Web3.toChecksumAddress(asset_addresses[asset.strip().upper()]) for asset in asset_names.split(",")]

# Create unstake transaction
transaction = contract.functions.unstake(asset_addresses_list, token_ids_list).buildTransaction({
    'from': wallet_address,
    'nonce': web3.eth.getTransactionCount(wallet_address),
    'gas': 2000000,
    'gasPrice': web3.toWei('50', 'gwei')
})

# Sign the transaction
signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send the transaction
tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Display transaction hash
print(f"Transaction sent! You can view it at https://etherscan.io/tx/{web3.toHex(tx_hash)}")
