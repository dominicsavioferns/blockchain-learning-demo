from brownie import SimpleStorage, accounts, config


def read_contract():
    # index 0 first deployment
    # index -1 last deployment
    simple_storage = SimpleStorage[-1]

    # ABI
    # Address
    print(simple_storage.retrieve())


def main():
    read_contract()
