import requests
import time

API_URLS = [
    "http://localhost:8080/names/1",
    "http://localhost:8080/names/2",
] * 1000

start_time = time.perf_counter()

for url in API_URLS:
    response = requests.get(url)
    # print(response.json())


end_time = time.perf_counter()
print(f"Duration: {round(end_time - start_time, 2)} seconds")
