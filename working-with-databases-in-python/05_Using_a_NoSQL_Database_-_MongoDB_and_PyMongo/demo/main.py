import datetime

import click
import requests

# from mongita import MongitaClientDisk
from pymongo import MongoClient


def get_coin_price(coin_id, currency):
    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies={currency}"
    )
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price


@click.group()
def cli():
    pass


@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="usd")
def show_coin_price(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")


@click.command()
@click.option("--coin_id")
@click.option("--currency")
@click.option("--amount", type=float)
@click.option("--sell", is_flag=True)
def add_investment(coin_id, currency, amount, sell):
    # Dictionary that represents the investment document
    investment_document = {
        "coin_id": coin_id,
        "currency": currency,
        "amount": amount,
        "sell": sell,
        "timestamp": datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
    }
    # Insert the investment document into the investments collection
    investments.insert_one(investment_document)

    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")


@click.command()
@click.option("--coin_id")
@click.option("--currency")
def get_investment_value(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    # Filter the document for the buys and sells
    buy_result = investments.find(
        {"coin_id": coin_id, "currency": currency, "sell": False}
    )
    sell_result = investments.find(
        {"coin_id": coin_id, "currency": currency, "sell": True}
    )
    # Mongita retrurns a list of documents, so we need to access the amount field
    buy_amount = sum(doc["amount"] for doc in buy_result)
    sell_amount = sum(doc["amount"] for doc in sell_result)

    total = buy_amount - sell_amount

    print(
        f"You own a total of {total} {coin_id} worth {total * coin_price:.2f} {currency.upper()}"
    )


@click.command()
@click.option("--csv_file")
def import_investments(csv_file):
    pass


cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investment_value)
cli.add_command(import_investments)

if __name__ == "__main__":
    # Initialize MongoDB client
    # client = MongitaClientDisk()
    client = MongoClient()
    # The protfolio database is an attribute of the client
    database = client.portfolio
    # The investments collection is an attribute of the database
    investments = database.investments

    cli()
