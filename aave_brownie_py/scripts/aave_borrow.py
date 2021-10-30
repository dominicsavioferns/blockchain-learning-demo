from scripts.helpful_scripts import get_account
from brownie import network, config, interface
from scripts.get_weth import get_weth
from web3 import Web3

# 0.1 ETH
amount = Web3.toWei(0.1, "ether")


def main():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]

    if network.show_active() in ["mainnet-fork-dev"]:
        get_weth()

    # ABI
    # Address
    lending_pool = get_lending_pool()

    # Approve sending out ERC20 tokens
    approve_erc20(amount, lending_pool.address, erc20_address, account)

    print("Depositing ETH to aave")
    txn = lending_pool.deposit(
        erc20_address, amount, account.address, 0, {"from": account}
    )
    txn.wait(1)
    print("Deposited")

    # how much can be borrowed
    borrowable_eth, total_debt = get_borowable_data(lending_pool, account)

    dai_eth_price = get_asset_price(
        config["networks"][network.show_active()]["dai_eth_price_feed"]
    )

    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    # borrowable eth => 95% of borrowable eth
    print(f"amount we are going to borrow {amount_dai_to_borrow} DAI")

    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_txn = lending_pool.borrow(
        dai_address,
        Web3.toWei(amount_dai_to_borrow, "ether"),
        1,
        0,
        account,
        {"from": account},
    )
    borrow_txn.wait(1)

    print("borrowed DAI!")
    borrowable_eth, total_debt = get_borowable_data(lending_pool, account)
    print(f"borrowable is now {borrowable_eth}")

    # repay back
    repay_all(amount, lending_pool, account)


def repay_all(amount, lending_pool, account):
    approve_erc20(
        Web3.toWei(amount, "ether"),
        lending_pool,
        config["networks"][network.show_active()]["dai_token"],
        account,
    )

    repay_txn = lending_pool.repay(
        config["networks"][network.show_active()]["dai_token"],
        amount,
        1,
        account.address,
        {"from": account},
    )
    repay_txn.wait(1)

    print("Repaid!!!")


def get_asset_price(price_feed_address):
    dai_eth_price_feed = interface.IAggregatorV3(price_feed_address)
    latest_price = dai_eth_price_feed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"dai-eth price {converted_latest_price}")
    return float(converted_latest_price)


def get_borowable_data(lending_pool, account):
    (
        toal_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    toal_collateral_eth = Web3.fromWei(toal_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")

    print(f"you have {available_borrow_eth} available borrow eth")
    print(f"you have {toal_collateral_eth} collateral eth")
    print(f"you have {total_debt_eth} total debt eth")

    return (float(available_borrow_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20 Token.")
    erc20 = interface.ERC20(erc20_address)
    txn = erc20.approve(spender, amount, {"from": account})
    txn.wait(1)
    print("Approved")
    return txn


# for interacting with aave
def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool
