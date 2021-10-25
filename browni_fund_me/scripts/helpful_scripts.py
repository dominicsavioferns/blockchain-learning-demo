from brownie import config, accounts, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_VALUE = 200000000000

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    print("Deploying Mocks...")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_VALUE, "ether"), {"from": get_account()}
        )

    print("Mocks deployed.")


# fork
# brownie networks add development mainnet-fork-dev cmd=ganache-cli host=http://127.0.0.1 fork='ALCHEMY APP KEY OR INFURA' accounts=10 mnemonic=brownie port=8545
