import json
from web3 import Web3
import time
import random

time_ot = 50   # диапазон для ожидания между кошельками
time_do = 300

# RPCs
w3 = Web3(Web3.HTTPProvider("https://mainnet.era.zksync.io"))
# ABI
abi = json.load(open('autodcaABI.json')) # ABI
nft_contract_address = w3.to_checksum_address('0x111f5DAB17D942ae5C0BA829cA913B806e6d3040') # контракт НФТ https://autodca.io/nft
nft_cotract = w3.eth.contract(address=nft_contract_address, abi=abi)


with open("privates.txt", "r") as f:
    keys_list = [row.strip() for row in f if row.strip()]
    numbered_keys = list(enumerate(keys_list, start=1))
    random.shuffle(numbered_keys) # перемешивание кошельков - можно закомментить

for wallet_number, PRIVATE_KEY in numbered_keys:

    account = w3.eth.account.from_key(PRIVATE_KEY)
    address = account.address

    print(time.strftime("%H:%M:%S", time.localtime()))
    print(f'[{wallet_number}] - {address}', flush=True)

    gas = random.randint(1290000, 1300000) # можно уменьшить значения

    nonce = w3.eth.get_transaction_count(address)

    tx_mint = nft_cotract.functions.mint(
            address
        ).build_transaction({
            'from': address,
            'gas': gas,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce
        })


    try:
        mint_txn = w3.eth.account.sign_transaction(tx_mint, PRIVATE_KEY)
        mint_txn_hash = w3.eth.send_raw_transaction(mint_txn.rawTransaction)
        print(f"Transaction: https://explorer.zksync.io/tx/{mint_txn_hash.hex()}")
        time.sleep(random.randint(time_ot, time_do))

    except Exception as err:
        print(f"Unexpected {err=}")
