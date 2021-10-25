from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)


def deploy_fund_me():
    active_network = network.show_active()
    account = get_account()

    print(f"Active Network {active_network}")

    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][active_network]["eth_to_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # pass price feed address to fundme constructor
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][active_network].get("verify"),
    )

    print(f"Contract deployed to {fund_me.address}")

    return fund_me


def main():
    deploy_fund_me()
