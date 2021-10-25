from brownie import accounts, SimpleStorage


def test_deploy():
    # Arrage
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    start_value = simple_storage.retrieve()
    expected_value = 0

    # Assert
    assert start_value == expected_value


def test_update_testing():
    # Arrage
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    expected_value = 15
    simple_storage.store(expected_value, {"from": account})

    # Assert
    assert expected_value == simple_storage.retrieve()
