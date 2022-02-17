from scripts.helpful_scripts import get_account, upgrade, encode_function_data
from brownie import (
    Box,
    network,
    ProxyAdmin,
    config,
    TransparentUpgradeableProxy,
    Contract,
    BoxV2,
)


def test_box_deploy():

    account = get_account()
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )
    box_encoded_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        # account.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    old_val_box = proxy_box.retrieve()

    # ______________________________________________#
    box_v2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    proxy = TransparentUpgradeableProxy[-1]
    proxy_admin = ProxyAdmin[-1]
    upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    old_val_boxv2 = proxy_box.retrieve({"from": account})
    proxy_box.increment({"from": account})
    updated_val = proxy_box.retrieve()
    assert old_val_boxv2 == 0
    assert old_val_box == 0
    assert old_val_box + 1 == updated_val


def main():
    test_box_deploy()
