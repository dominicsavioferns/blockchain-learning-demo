from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    # account = accounts.add(config["wallets"]["from_key"])
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    favourite_number = simple_storage.retrieve()
    print(favourite_number)

    transaction = simple_storage.store(8, {"from": account})
    transaction.wait(1)
    print(transaction)

    favourite_number = simple_storage.retrieve()
    print("updated value: ", favourite_number)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()


# to deploy to rinkeby network
# brownie run .\scripts\deploy.py --network rinkeby
