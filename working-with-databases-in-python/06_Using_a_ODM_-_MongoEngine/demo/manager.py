import datetime
import random

from mongoengine import connect, Document
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


def _select_investment():
    investment_coins = Investment.objects.all().fields(coin=1)
    for index, coin in enumerate(investment_coins):
        print(f"{index + 1}: {coin.coin}")
    selected_investment_index = int(input("Select an investment: ")) - 1
    selected_investment_oid = investment_coins[selected_investment_index].id
    return Investment.objects(id=selected_investment_oid).first()


def _seed_data():
    data = [
        ("bitcoin", "USD", 1.0, False),
        ("ethereum", "GBP", 10.0, True),
        ("dogecoin", "EUR", 100.0, False),
    ]

    for row in data:
        Investment(
            coin=row[0],
            currency=row[1],
            amount=row[2],
            sell=row[3],
            timestamp=datetime.datetime.now()
            - datetime.timedelta(
                days=random.randint(0, 7),
                minutes=random.randint(0, 60),
                seconds=random.randint(0, 60),
            ),
        ).save()


@click.group()
def cli():
    pass


@click.command(help="Clear the database")
def clear_data():
    Investment.drop_collection()

    print("Cleared data!")


@click.command(
    help="Seed the database with sample data, use the --force flag to ignore existing data"
)
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
@click.option(
    "--sell", is_flag=True, default=False, help="If this is a sell (default is False)"
)
def add_investment(coin, currency, amount, sell):
    investment = Investment(coin=coin, currency=currency, amount=amount, sell=sell)
    investment.save()

    print(f"Added {'buy' if not sell else 'sell'} for {amount} {coin} in {currency}")


@click.command(help="See the details of an investment")
def view_investment():
    selected_investment = _select_investment()
    coin_price = get_coin_prices(
        [selected_investment.coin], selected_investment.currency.lower()
    )[selected_investment.coin]
    print(
        f"You {'bought' if not selected_investment.sell else 'sold'} {selected_investment.amount} {selected_investment.coin} for {coin_price * selected_investment.amount} {selected_investment.currency}"
    )


cli.add_command(add_investment)
cli.add_command(clear_data)
cli.add_command(seed_data)
cli.add_command(view_investment)

if __name__ == "__main__":
    connect("portfolio_me")
    cli()
