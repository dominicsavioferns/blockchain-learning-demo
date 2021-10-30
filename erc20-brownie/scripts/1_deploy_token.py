from brownie import DOMToken
from toolz.itertoolz import get
from scripts.helpful_scripts import get_account
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    print(account)
    dom_token = DOMToken.deploy(initial_supply, {"from": account})
    print(dom_token.name())
