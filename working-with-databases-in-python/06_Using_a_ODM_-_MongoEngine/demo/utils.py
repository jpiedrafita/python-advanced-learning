import datetime
import random

import requests


def get_random_datetime():
    return datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 7))


def get_coin_prices(coin_ids, currency):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_ids)}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_prices = dict([(coin_id, data[coin_id][currency]) for coin_id in data])
    return coin_prices


def seed_data(collection):
    collection.insert_many(
        [
            {
                "name": "Bulls",
                "metadata": {
                    "description": "Coins to buy",
                    "currency": "usd",
                    "date_created": get_random_datetime(),
                },
                "coins": [
                    {
                        "coin": "bitcoin",
                        "note": "The most popular coin",
                        "date_added": get_random_datetime(),
                    },
                    {
                        "coin": "ethereum",
                        "note": "The second most popular coin",
                        "date_added": get_random_datetime(),
                    },
                ],
            },
            {
                "name": "Bears",
                "metadata": {
                    "description": "Coins to hold or sell",
                    "currency": "usd",
                    "date_created": get_random_datetime(),
                },
                "coins": [
                    {
                        "coin": "solana",
                        "note": "Don't sell this one yet",
                        "date_added": get_random_datetime(),
                    }
                ],
            },
        ]
    )
