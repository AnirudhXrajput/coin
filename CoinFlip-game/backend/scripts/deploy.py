import os
from web3 import Web3
from solcx import compile_standard, install_solc

install_solc('0.8.0')

with open("../contracts/CoinFlip.sol", "r") as file:
    coinflip_file = file.read()

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {"CoinFlip.sol": {"content": coinflip_file}},
    "settings": {
        "outputSelection": {
            "*": {
                "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
            }
        }
    }
})

bytecode = compiled_sol['contracts']['CoinFlip.sol']['CoinFlip']['evm']['bytecode']['object']
abi = compiled_sol['contracts']['CoinFlip.sol']['CoinFlip']['abi']

w3 = Web3(Web3.HTTPProvider(os.getenv('RINKEBY_URL')))
chain_id = 4
my_address = os.getenv('MY_ADDRESS')
private_key = os.getenv('PRIVATE_KEY')

CoinFlip = w3.eth.contract(abi=abi, bytecode=bytecode)
nonce = w3.eth.getTransactionCount(my_address)

transaction = CoinFlip.constructor().buildTransaction({
    'chainId': chain_id,
    'gas': 2000000,
    'gasPrice': w3.toWei('20', 'gwei'),
    'nonce': nonce,
})

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
tx_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(f"Contract deployed at address: {tx_receipt.contractAddress}")
