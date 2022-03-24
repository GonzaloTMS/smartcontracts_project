import time
from scripts.helful_scripts import get_account, get_contract, fund_with_link
from brownie import Lottery, config, network, Oracle


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        Oracle[-1],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery contract")
    return lottery


def deploy_oracle():
    account = get_account()
    oracle = Oracle.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed oracle contract")
    return oracle


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("The lottery is started")


def buy_lotteryTicket(id=None, index=None):
    account = get_account(id=id)
    lottery = Lottery[-1]
    value = lottery.getTicketPrice() + 100000000
    tx = lottery.buyTicket({"from": account, "value": value})
    tx.wait(1)
    print("You entered de lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(20)
    print(f"{lottery.last_winner()} is the new winner")
    print(f"{lottery.random_number()}RANDOM")


def main():
    deploy_oracle()
    deploy_lottery()
    print("Loteria 1")
    print("=========")
    start_lottery()
    buy_lotteryTicket()
    buy_lotteryTicket(id=1)
    buy_lotteryTicket(id=2)
    end_lottery()

    """
    lottery = Lottery[-1]
    print(lottery.random_number())
    tx = oracle.newRequest("http://localhost:8080/api/random", {"from": account})
    tx.wait(1)
    print("evento emitido")
    time.sleep(30)
    random_number = oracle.getValue(5)
    print(random_number)
    print("Loteria 1")
    print("=========")
    start_lottery()
    buy_lotteryTicket()
    end_lottery()
    print("Loteria 2")
    print("=========")
    start_lottery()
    buy_lotteryTicket(index=0)
    buy_lotteryTicket(index=1)
    buy_lotteryTicket(index=2)
    buy_lotteryTicket(index=3)
    buy_lotteryTicket(index=4)
    buy_lotteryTicket(index=5)
    end_lottery()
    print("Loteria 3")
    print("=========")
    start_lottery()
    buy_lotteryTicket(index=0)
    buy_lotteryTicket(index=1)
    buy_lotteryTicket(index=2)
    buy_lotteryTicket(index=3)
    buy_lotteryTicket(index=4)
    buy_lotteryTicket(index=5)
    end_lottery()
    """
