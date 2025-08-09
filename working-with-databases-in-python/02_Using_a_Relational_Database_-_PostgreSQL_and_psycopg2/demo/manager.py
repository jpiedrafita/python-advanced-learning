from dataclasses import dataclass
import csv

import click
import requests
import psycopg2
import psycopg2.extras


@dataclass
class Investment:
    id: int
    coin: str
    currency: str
    amount: float


def get_connection():
    connection = psycopg2.connect(
        database="manager",
        user="postgres",
        password="PGpassword",
        host="localhost",
    )
    return connection


@click.group()
def cli():
    pass


@cli.command()
@click.option("--coin", prompt=True)
@click.option("--currency", prompt=True)
@click.option("--amount", prompt=True)
def new_investment(coin, currency, amount):
    # Create a new investment in the database normalizing to lowercase
    stmt = f"""
        insert into investment (
            coin, currency, amount
        ) values (
            '{coin.lower()}', '{currency.lower()}', {amount}
        )
    """
    # Get the connection to the database and cursor
    connection = get_connection()
    cursor = connection.cursor()
    # Execute the SQL statement and commit
    cursor.execute(stmt)
    connection.commit()
    # Close the cursor and connection
    cursor.close()
    connection.close()
    print(f"Added investment for {amount} {coin} in {currency}.")


@click.command()
@click.option("--filename")
def import_investments(filename):
    # Statement to insert multiple rows into the investment table taking the values as a parameter
    stmt = "insert into investment (coin, currency, amount) values %s"

    # Get the connection to the database and cursor
    connection = get_connection()
    cursor = connection.cursor()

    # Read the CSV file and prepare the data for insertion omiting ID
    with open(filename, "r") as f:
        coin_reader = csv.reader(f)
        rows = [[x.lower() for x in row[1:]] for row in coin_reader]
    print(f"Added {len(rows)} investments from {filename}.")

    # Use psycopg2.extras.execute_values to insert multiple rows at once
    psycopg2.extras.execute_values(cursor, stmt, rows)

    # Commit the changes and close the cursor and connection
    connection.commit()
    cursor.close()
    connection.close()


@click.command()
@click.option(
    "--currency",
)
def view_investments(currency):
    # Get the connection to the database and cursor using RealDictCursor for easy access
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Create a SQL query to select all investments
    stmt = "select * from investment"

    # If currency is provided, filter the investments by currency, by appending a WHERE clause
    if currency:
        stmt += f" where currency = '{currency.lower()}'"

    # Use the cursor to execute the SQL statement
    cursor.execute(stmt)

    # For each row in the result, create an Investment object
    data = [Investment(**dict(row)) for row in cursor.fetchall()]

    # Close the cursor and connection
    cursor.close()
    connection.close()

    # Get the coin names and currencies from the data, unique them, and fetch their current prices from CoinGecko
    coins = set([row.coin for row in data])
    currencies = set([row.currency for row in data])
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coins)}&vs_currencies={','.join(currencies)}"
    coin_data = requests.get(url).json()

    # For each investment, get the price for the coin and compute the total value in the specified currency
    for investment in data:
        coin_price = coin_data[investment.coin][investment.currency.lower()]
        coin_total = investment.amount * coin_price
        print(
            f"{investment.amount} ({investment.coin}) in {investment.currency} is worth {coin_price:.2f} = {coin_total:.2f} {currency}"
        )


cli.add_command(new_investment)
cli.add_command(import_investments)
cli.add_command(view_investments)

if __name__ == "__main__":
    cli()
