from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

# import environment variables
load_dotenv()

# install solcx version
install_solc("0.6.0")

# read solidity code
with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# compile solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourcemap"]}
            }
        },
    },
    solc_version="0.6.0",
)

# output compiled code to file
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)


# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# connect to Ganache
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_URL")))
chain_id = int(os.getenv("CHAIN_ID"))
my_address = os.getenv("MY_ADDRESS")
private_key = os.getenv("PRIVATE_KEY")


def get_txn_params():
    return {"chainId": chain_id, "from": my_address, "nonce": get_nonce()}


def get_nonce():
    return w3.eth.getTransactionCount(my_address)


# Create contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get latestes transaction
nonce = get_nonce()

print("nonce: ", nonce)

# build a transaction
# Sign a transaction
# Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(get_txn_params())

signed_txn = w3.eth.account.sign_transaction(transaction, private_key)

txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# transaction receipt
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)


# working with contract, always need
# contract address
# contract ABI
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# call -> simulate making the call and getting return value
# transact -> make state change
print("Initial favouriteNumber value:", simple_storage.functions.retrieve().call())

# make a state change
# need to sign every new transaction
print("Set new value to favouriteNumber")
store_txn = simple_storage.functions.store(8).buildTransaction(get_txn_params())
signed_store_txn = w3.eth.account.sign_transaction(store_txn, private_key)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)

print("New favouriteNumber value:", simple_storage.functions.retrieve().call())
