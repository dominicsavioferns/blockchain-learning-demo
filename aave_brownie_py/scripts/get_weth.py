from scripts.helpful_scripts import get_account
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH
    """
    # ABI
    # Address
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])

    # deposit eth to get weth
    txn = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    txn.wait(1)
    print(f"Recieved 0.1 Weth")
    return txn
