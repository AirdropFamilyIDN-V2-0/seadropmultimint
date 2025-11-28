#!/usr/bin/env python3
from web3 import Web3, HTTPProvider
from web3 import __version__ as web3_version
from packaging.version import Version
from eth_account import Account
import time, sys, json

# Require exact Web3.py 7.12.0
REQUIRED_WEB3 = "7.12.0"
if web3_version != REQUIRED_WEB3:
    print(f"ERROR: Web3.py version must be EXACTLY {REQUIRED_WEB3}")
    print(f"You have: {web3_version}")
    print("Run: pip uninstall web3")
    print("Run: pip install web3==7.12.0")
    sys.exit(1)
print(f"Web3.py version OK: {web3_version}")

# Constants
SEA_DROP_ADDR = "0x00005EA00Ac477B1030CE78506496e8C2dE24bf5"
MULTIMINT_ADDR = "0x0000419B4B6132e05DfBd89F65B165DFD6fA126F"
SUPPORTED_CHAIN_IDS = {1, 10, 42161, 8453, 143, 137, 2741, 43114, 80094, 999}

# Minimal ABIs (only what's needed)
SEA_ABI = json.loads('[{"inputs":[{"internalType":"address","name":"nftContract","type":"address"}],"name":"getPublicDrop","outputs":[{"components":[{"internalType":"uint80","name":"mintPrice","type":"uint80"},{"internalType":"uint48","name":"startTime","type":"uint48"},{"internalType":"uint48","name":"endTime","type":"uint48"},{"internalType":"uint16","name":"maxTotalMintableByWallet","type":"uint16"},{"internalType":"uint16","name":"feeBps","type":"uint16"},{"internalType":"bool","name":"restrictFeeRecipients","type":"bool"}],"internalType":"struct PublicDrop","name":"","type":"tuple"}],"stateMutability":"view","type":"function"}]')
MULTI_ABI = json.loads('[{"inputs":[{"internalType":"uint256","name":"total","type":"uint256"},{"internalType":"address","name":"nftaddress","type":"address"}],"name":"mintMulti","outputs":[],"stateMutability":"payable","type":"function"}]')

# Symbol map for native token display
SYMBOLS = {
    1: "ETH", 10: "ETH", 42161: "ETH", 8453: "ETH",
    137: "POL", 43114: "AVAX", 143: "MON", 2741: "ETH",
    80094: "BERA", 999: "HYPE"
}

# Helpers
def to_checksum(addr: str) -> str:
    return Web3.to_checksum_address(addr)

def parse_gas_price_gwei_input(inp: str, w3: Web3) -> int:
    try:
        if inp is None:
            base = w3.eth.gas_price
            return int(base * 1.2)
        s = inp.strip()
        if s == "":
            base = w3.eth.gas_price
            return int(base * 1.2)
        s_norm = s.lower().replace("gwei", "").strip()
        gwei_value = float(s_norm)
        wei = int(gwei_value * 1_000_000_000)
        return wei
    except Exception as e:
        print("Invalid gas price input; falling back to node gas price * 1.2. (e)", e)
        base = w3.eth.gas_price
        return int(base * 1.2)

def gwei_from_wei(wei: int) -> float:
    return wei / 1e9

def sign_send_wait(w3: Web3, acct: Account, tx: dict, timeout=600):
    try:
        if "nonce" not in tx:
            tx["nonce"] = w3.eth.get_transaction_count(acct.address)
        if "chainId" not in tx:
            tx["chainId"] = w3.eth.chain_id
        signed = acct.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        print("Sent Tx :", tx_hash.hex())
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        return receipt
    except Exception as e:
        raise

# Main - Mint Loop Only
print(f'Auto SeaDrop MultiMint V2 By ADFMIDN Team')
print(f'')
def main():
    try:
        rpc = input("Input RPC URL : ").strip()
        if not rpc:
            print("RPC URL Required.")
            return
        w3 = Web3(HTTPProvider(rpc, request_kwargs={"timeout": 60}))
        connected = w3.is_connected()
        print("Connected : ", connected)
        if not connected:
            print("Unable To Connect To RPC! Exiting...")
            return

        chain_id = w3.eth.chain_id
        print("chainId =", chain_id)
        if chain_id not in SUPPORTED_CHAIN_IDS:
            print("Chain Not Supported. Supported : ", SUPPORTED_CHAIN_IDS)
            return
        native_symbol = SYMBOLS.get(chain_id, "ETH")

        # Contracts
        sea_drop = to_checksum(SEA_DROP_ADDR)
        multimint = to_checksum(MULTIMINT_ADDR)
        sea_contract = w3.eth.contract(address=sea_drop, abi=SEA_ABI)
        multi_contract = w3.eth.contract(address=multimint, abi=MULTI_ABI)

        # Wallet
        pk = input("Input Private Key EVM : ").strip()
        acct = Account.from_key(pk)
        print("Using Address : ", acct.address)

        # Gas price
        gas_inp = input("Input Custom GWEI/Gas Price ( 0.01/1/10/100 ) Or Leave Blank [Default] : ")
        gas_price = parse_gas_price_gwei_input(gas_inp, w3)
        print(f"Using Gas Price : {gwei_from_wei(gas_price)}")

        # Mint inputs
        nft_raw = input("Input NFT Contract Address : ").strip()
        nft_addr = to_checksum(nft_raw)
        total = int(input("Total Mint NFT : ").strip())

        # read price
        try:
            tup = sea_contract.functions.getPublicDrop(nft_addr).call()
            price = int(tup[0])
        except Exception as e:
            print("Failed Read Price From SeaDrop : ", e)
            return

        required_total_cost = price * total
        price_native = float(price) / 1e18
        total_native = float(required_total_cost) / 1e18
        print(f"Price Per Token : {price_native:g} {native_symbol}")
        print(f"Total Cost For {total} : {total_native:g} {native_symbol}")

        bal = w3.eth.get_balance(acct.address)
        bal_native = float(bal) / 1e18
        print(f"Wallet Native Balance: {bal_native:g} {native_symbol}")
        if bal < required_total_cost:
            print("Not Enought Native Balance! Exiting...")
            return

        attempt = 0
        while True:
            attempt += 1
            try:
                print(f"Attempt #{attempt}: Building Mint TX...")
                value = required_total_cost
                nonce = w3.eth.get_transaction_count(acct.address)
                func = multi_contract.functions.mintMulti(total, nft_addr)

                # estimate gas (no fallback)
                estimated_gas = func.estimate_gas({"from": acct.address, "value": value})
                print("Estimated gas:", estimated_gas)

                tx = func.build_transaction({
                    "chainId": chain_id,
                    "from": acct.address,
                    "value": value,
                    "gas": int(estimated_gas * 1.2),
                    "gasPrice": gas_price,
                    "nonce": nonce
                })

                receipt = sign_send_wait(w3, acct, tx)
                print("Mint Receipt Status : ", receipt.status)
                if receipt.status == 1:
                    print("Mint TX Succeeded : ", receipt.transactionHash.hex())
                    break
                else:
                    print("Mint TX Failed Retrying...")
                    # time.sleep(3)
                    continue

            except Exception as e:
                print("Mint Attempt Exception : ", e)
                print("Retrying...")
                # time.sleep(3)
                continue

    except Exception as e:
        print("Fatal Error : ", e)

if __name__ == "__main__":
    main()