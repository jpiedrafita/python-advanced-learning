import datetime
import csv

import click
import requests
import sqlite3


# SQL command to create the investments table if it doesn't exist
CREATE_INVESTMENTS_SQL = """
CREATE TABLE IF NOT EXISTS investments (
    coin_id TEXT NOT NULL,
    currency TEXT NOT NULL,
    amount REAL NOT NULL,
    sell INTEGER NOT NULL,
    date TEXT NOT NULL
);
"""


def get_coin_price(coin_id, currency):
    url = (
        f"https://api.coingecko.com/api/v3/simple/price"
        f"?ids={coin_id}&vs_currencies={currency}"
    )
    data = requests.get(url).json()
    coin_price = data[coin_id][currency]
    return coin_price


# A command group allowing for multiple commands to be added later
@click.group()
def cli():
    pass


@click.command()
@click.option("--coin_id", default="bitcoin")
@click.option("--currency", default="usd")
def show_coin_price(coin_id, currency):
    coin_price = get_coin_price(coin_id, currency)
    print(f"The price of {coin_id} is {coin_price:.2f} {currency.upper()}")


# cli funcion to add an investment (buy or sell)
@click.command()
@click.option("--coin_id")
@click.option("--currency")
@click.option("--amount", type=float)
@click.option("--sell", is_flag=True)
def add_investment(coin_id, currency, amount, sell):
    # Parametrized SQL query to insert a new investment record
    sql = "INSERT INTO investments VALUES (?, ?, ?, ?, ?);"
    # Row values into a tuple
    values = (coin_id, currency, amount, sell, datetime.datetime.now().isoformat())
    # Execute the SQL command with the provided values
    cursor.execute(sql, values)
    # Commit the changes to the database
    database.commit()
    if sell:
        print(f"Added sell of {amount} {coin_id}")
    else:
        print(f"Added buy of {amount} {coin_id}")


# Function to get the total investment for a specific coin and currency
@click.command()
@click.option("--coin_id")
@click.option("--currency")
def get_investment_value(coin_id, currency):
    # Get the current price of the coin in the specified currency
    coin_price = get_coin_price(coin_id, currency)
    print(f"Current price of {coin_id} in {currency} is {coin_price:.2f}")
    # Parametrized SQL Query to get the investments for buy and sell
    sql = """SELECT amount
    FROM investments
    WHERE coin_id = ?
    AND currency = ?
    AND sell=?;"""
    # Get the buy/sell investements
    buy_result = cursor.execute(sql, (coin_id, currency, False)).fetchall()
    sell_result = cursor.execute(sql, (coin_id, currency, True)).fetchall()
    # As fetchall returns a list of tuples, we need to sum the amounts
    buy_amount = sum(row[0] for row in buy_result)
    sell_amount = sum(row[0] for row in sell_result)
    total = buy_amount - sell_amount
    print(
        f"You own a total of {total} {coin_id} worth {total * coin_price:.2f} {currency.upper()}"
    )


@click.command()
@click.option("--csv_file")
def import_investments(csv_file):
    with open(csv_file, "r") as f:
        rdr = csv.reader(f, delimiter=",")
        # Turns each row into a list
        rows = list(rdr)
        # Parametrized SQL query to insert a new investment record
        sql = "INSERT INTO investments VALUES (?, ?, ?, ?, ?);"
        # Instead of iterating over the rows, we can use executemany to insert all rows at once
        cursor.executemany(sql, rows)
        database.commit()
        print(f"Imported {len(rows)} investments from {csv_file}")


# Register the command with the CLI group
cli.add_command(show_coin_price)
cli.add_command(add_investment)
cli.add_command(get_investment_value)
cli.add_command(import_investments)

# Register the CLI group as the main entry point
if __name__ == "__main__":
    # Connect to the SQLite database and create the investments table if it doesn't exist
    database = sqlite3.connect("portfolio.db")
    # Create a cursor object to execute SQL commands
    cursor = database.cursor()
    # Create the investments table
    cursor.execute(CREATE_INVESTMENTS_SQL)
    cli()
