import datetime
import random

from mongoengine import connect, Document, EmbeddedDocument
from mongoengine import fields
import click

from utils import get_coin_prices


class Investment(Document):
    coin = fields.StringField(max_length=32)
    currency = fields.StringField(max_length=3)
    amount = fields.FloatField(min_value=0.00001)
    timestamp = fields.DateTimeField(default=datetime.datetime.now)
    sell = fields.BooleanField(default=False)

    def __str__(self):
        return f"<Investment | coin: {self.coin}, currency: {self.currency}, amount: {self.amount}>"


class WatchlistMetadata(EmbeddedDocument):
    currency = fields.StringField(max_length=3)
    description = fields.StringField()
    date_created = fields.DateField(default=datetime.datetime.now().date)


class WatchlistCoin(EmbeddedDocument):
    coin = fields.StringField(max_length=32)
    note = fields.StringField()
    date_added = fields.DateField(default=datetime.datetime.now().date)


class Watchlist(Document):
    name = fields.StringField(max_length=256)
    metadata = fields.EmbeddedDocumentField(WatchlistMetadata)
    coins = fields.EmbeddedDocumentListField(WatchlistCoin)

    def __str__(self):
        return f"<Watchlist name={self.name}, currency={self.metadata.currency} with {len(self.coins)} coin(s)>"


def _select_investment():
    investment_coins = Investment.objects.all().fields(coin=1)
    for index, coin in enumerate(investment_coins):
        print(f"{index + 1}: {coin.coin}")
    selected_investment_index = int(input("Select an investment: ")) - 1
    selected_investment_oid = investment_coins[selected_investment_index].id
    return Investment.objects(id=selected_investment_oid).first()


def _select_watchlist():
    watchlist_names = Watchlist.objects.all().fields(name=1)
    for index, name in enumerate(watchlist_names):
        print(f"{index + 1}: {name.name}")
    selected_watchlist_index = int(input("Select a watchlist: ")) - 1
    selected_watchlist_oid = watchlist_names[selected_watchlist_index].id
    return Watchlist.objects(id=selected_watchlist_oid).first()


def _seed_data():
    data = [
        ("bitcoin", "USD", 1.0, False),
        ("ethereum", "GBP", 10.0, True),
        ("dogecoin", "EUR", 100.0, False)
    ]

    watchlist_data = [
        ("Bulls", "Coins to buy", "USD", [
         ("bitcoin", "Bitcoin is number one!"), ("ethereum", "Ethereum is number two!")]),
        ("Bears", "Coins to sell", "GBP", [("solana", "Meh ...")])
    ]

    for row in data:
        Investment(
            coin=row[0],
            currency=row[1],
            amount=row[2],
            sell=row[3],
            timestamp=datetime.datetime.now() - datetime.timedelta(
                days=random.randint(0, 7), minutes=random.randint(0, 60), seconds=random.randint(0, 60)
            )).save()

    for row in watchlist_data:
        Watchlist(
            name=row[0],
            metadata=WatchlistMetadata(description=row[1], currency=row[2]),
            coins=[WatchlistCoin(coin=coin[0], note=coin[1])
                   for coin in row[3]]
        ).save()


@click.group()
def cli():
    pass


@click.command(help="Clear the database")
def clear_data():
    Investment.drop_collection()
    Watchlist.drop_collection()

    print("Cleared data!")


@click.command(help="Seed the database with sample data, use the --force flag to ignore existing data")
@click.option("--force", is_flag=True, default=False)
def seed_data(force):
    if force:
        _seed_data()
    elif Investment.objects.count() > 0:
        print("Data not empty!  Use --force flag to seed database")
    else:
        _seed_data()


@click.command(help="Add a new investment to the portfolio")
@click.option("--coin", prompt=True, help="The name of the coin")
@click.option("--currency", prompt=True, help="The fiat currency to show prices in")
@click.option("--amount", prompt=True, help="The purchase amount")
@click.option("--sell", is_flag=True, default=False, help="If this is a sell (default is False)")
def add_investment(coin, currency, amount, sell):
    investment = Investment(
        coin=coin,
        currency=currency,
        amount=amount,
        sell=sell
    )
    investment.save()

    print(
        f"Added {'buy' if not sell else 'sell'} for {amount} {coin} in {currency}")


@click.command(help="See the details of an investment")
def view_investment():
    selected_investment = _select_investment()
    coin_price = get_coin_prices([selected_investment.coin], selected_investment.currency.lower())[
        selected_investment.coin]
    print(f"You {'bought' if not selected_investment.sell else 'sold'} {selected_investment.amount} {selected_investment.coin} for {coin_price * selected_investment.amount} {selected_investment.currency}")


@click.command(help="Add a new watchlist to the portfolio")
@click.option("--name", help="The name of the watchlist", prompt=True)
@click.option("--description", help="The description of the watchlist", prompt=True)
@click.option("--currency", help="The currency to display coin prices in", prompt=True)
def add_watchlist(name, description, currency):
    metadata = WatchlistMetadata(currency=currency, description=description)
    watchlist = Watchlist(name=name, metadata=metadata, coins=[])
    watchlist.save()

    print(f"Added watchlist {name}")


@click.command(help="View the coins in a watchlist")
def view_watchlist():
    selected_watchlist = _select_watchlist()
    coins = [coin.coin for coin in selected_watchlist.coins]
    coin_prices = get_coin_prices(
        coins, selected_watchlist.metadata.currency.lower())
    print(
        f"Watchlist: {selected_watchlist.name} in {selected_watchlist.metadata.currency}")
    print(f"{selected_watchlist.metadata.description}")
    print("Coins: ")
    for index, coin in enumerate(coins):
        print(f"{index + 1}: {coin} | {coin_prices[coin]}")
    print("Prices provided by CoinGecko")


@click.command(help="Add a coin to a watchlist")
@click.option("--coin", help="The coin to add", prompt=True)
@click.option("--note", help="A note", prompt=True)
def add_coin(coin, note):
    selected_watchlist = _select_watchlist()
    selected_watchlist.coins.append(
        WatchlistCoin(coin=coin, note=note)
    )
    selected_watchlist.save()

    print(f"Added {coin} to {selected_watchlist.name}")


cli.add_command(add_coin)
cli.add_command(add_investment)
cli.add_command(add_watchlist)
cli.add_command(clear_data)
cli.add_command(seed_data)
cli.add_command(view_watchlist)
cli.add_command(view_investment)

if __name__ == "__main__":
    connect("portfolio_me")
    cli()
