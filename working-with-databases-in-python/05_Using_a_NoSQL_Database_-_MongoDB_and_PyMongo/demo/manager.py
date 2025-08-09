import datetime

import click
from bson import ObjectId
from pymongo import MongoClient

from utils import get_coin_prices
from utils import seed_data as utils_seed_data


# Connect to the MongoDB database default local client
client = MongoClient()
# We get the portfolio database and the watchlists collection in portfolio database
portfolio = client.portfolio
watchlists = portfolio.watchlists


def _get_all_watchlist_names():
    return list(watchlists.find({}, {"name": 1}))


def _select_watchlist(watchlist_names):
    for index, watchlist in enumerate(watchlist_names):
        print(f"{index + 1}: {watchlist['name']}")
    selected_watchlist_index = int(input("Select a watchlist: ")) - 1
    selected_watchlist_id = watchlist_names[selected_watchlist_index]["_id"]
    return watchlists.find_one({"_id": ObjectId(selected_watchlist_id)})


def _select_coin_from_watchlist(watchlist):
    for index, coin in enumerate(watchlist["coins"]):
        print(f"{index + 1}: {coin['coin']}")
    selected_coin_index = int(input("Select a coin: ")) - 1
    return watchlist["coins"][selected_coin_index]


def _add_coin_to_watchlist(watchlist_oid, coin):
    filter = {"_id": ObjectId(watchlist_oid)}
    update = {"$push": {"coins": coin}}
    watchlists.update_one(filter, update)


def _remove_coin_from_watchlist(watchlist_oid, selected_coin):
    filter = {"_id": ObjectId(watchlist_oid)}
    update = {"$pull": {"coins": {"coin": selected_coin}}}
    watchlists.update_one(filter, update)


@click.group()
def cli():
    pass


# Utility for dropping the watchlists collection
@click.command(help="Clear the database")
def clear_data():
    portfolio.drop_collection("watchlists")

    print("All data cleared!")


@click.command(help="Seed the database")
@click.option("--force", is_flag=True, help="Seed even if database is not empty")
def seed_data(force):
    if force:
        utils_seed_data(watchlists)
    elif watchlists.count_documents({}) > 0:
        print(
            "The database is not empty, use the --force option or the clear-data command"
        )
    else:
        utils_seed_data(watchlists)


@click.command(help="Add a new watchlist to the portfolio")
@click.option("--name", prompt=True, help="Name of the watchlist")
@click.option("--description", prompt=True, help="Description of the watchlist")
@click.option("--currency", prompt=True, help="Currency to display prices")
def add_watchlist(name, description, currency):
    metadata = {
        "description": description,
        "currency": currency,
        "date_added": datetime.datetime.now(),
    }
    # The netadata is embedded as a field of the watchlist document
    watchlist = {"name": name, "metadata": metadata, "coins": []}
    watchlists.insert_one(watchlist)

    print(f"Added new {name} watchlist")


@click.command(help="Add a new coin to a watchlist")
@click.option("--coin", prompt=True, help="The coin to add")
@click.option("--note", prompt=True, help="A note")
def add_coin(coin, note):
    selected_watchlist = _select_watchlist(_get_all_watchlist_names())
    _add_coin_to_watchlist(
        selected_watchlist["_id"],
        {"coin": coin, "note": note, "date_added": datetime.datetime.now()},
    )
    print(f"Added {coin} to {selected_watchlist['name']}")


@click.command(help="Remove a coin from a watchlist")
def remove_coin():
    selected_watchlist = _select_watchlist(_get_all_watchlist_names())
    selected_coin = _select_coin_from_watchlist(selected_watchlist)
    _remove_coin_from_watchlist(selected_watchlist["_id"], selected_coin["coin"])
    print(f"Removed {selected_coin['coin']} from {selected_watchlist['name']}")


@click.command(help="View the coins and current prices of a watchlist")
def view_watchlist():
    selected_watchlist = _select_watchlist(_get_all_watchlist_names())

    print(
        f"Watchlist: {selected_watchlist['name']} in {selected_watchlist['metadata']['currency']}"
    )
    print(f"{selected_watchlist['metadata']['description']}")
    print(f"{'-' * 25}")
    print("Coins:")
    coin_prices = get_coin_prices(
        [coin["coin"] for coin in selected_watchlist["coins"]],
        selected_watchlist["metadata"]["currency"],
    )
    for index, coin in enumerate(selected_watchlist["coins"]):
        print(f"{str(index + 1).rjust(3, ' ')}: {coin['coin']} - {coin['note']}")
        print(f"     Current price: {coin_prices[coin['coin']]}")
    print("Prices provided by CoinGecko")


cli.add_command(add_coin)
cli.add_command(add_watchlist)
cli.add_command(clear_data)
cli.add_command(remove_coin)
cli.add_command(seed_data)
cli.add_command(view_watchlist)


if __name__ == "__main__":
    cli()
