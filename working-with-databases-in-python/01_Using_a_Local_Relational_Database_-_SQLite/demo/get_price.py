import requests

coin_id = "bitcoin"
currency = "usd"

url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies={currency}"

data = requests.get(url).json()

coin_price = data[coin_id][currency]

print(coin_price)
