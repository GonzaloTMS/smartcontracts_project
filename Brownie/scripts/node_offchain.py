import json
import requests
from web3 import Web3
import asyncio
from brownie import Lottery, Oracle, network, config
from scripts.helful_scripts import (
    get_account,
    FORKED_LOCAL_ENVIROMENTS,
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
)

# add your blockchain connection information
ganache_url = "http://localhost:8545"
infura_url = "https://rinkeby.infura.io/v3/85255d60dc214513a8eef637d7c284ce"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract address and abi

contract_address = str(Lottery[-1])
contract_abi = Lottery.abi
contract = web3.eth.contract(address=contract_address, abi=contract_abi)


def handle_event(event):
    # First we extract id and url of the event
    event_json = Web3.toJSON(event)
    id = event["args"]["id"]
    url = event["args"]["url"]
    print("ID:", id)
    # Now, we send a get to URL
    response_API = requests.get(url)
    # We extract data from responese
    data = response_API.text
    parse_json = json.loads(data)
    # We get the random_number
    random_number = parse_json["value"]
    print("Random number", random_number)
    # TESTNET
    if network.show_active() in FORKED_LOCAL_ENVIROMENTS:
        raw_transaction = contract.functions.updateRequest(
            id, random_number
        ).buildTransaction(
            {
                "from": "0xbB8147F66FaF71A5bA41E5bD074d6562bd9DB362",
                "nonce": web3.eth.getTransactionCount(
                    "0xbB8147F66FaF71A5bA41E5bD074d6562bd9DB362"
                ),
            }
        )
        signed = web3.eth.account.signTransaction(
            raw_transaction,
            config["wallets"]["from_key"],
        )
        receipt = web3.eth.sendRawTransaction(signed.rawTransaction)
        web3.eth.waitForTransactionReceipt(receipt)
    # GANACHE
    else:
        print("Nada aun")

    print("Random number stored in the blockchain")


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "NewRequest" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for NewRequest in event_filter.get_new_entries():
            handle_event(NewRequest)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "NewRequest" event for Lottery contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.NewRequest.createFilter(fromBlock="latest")
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(asyncio.gather(log_loop(event_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()
