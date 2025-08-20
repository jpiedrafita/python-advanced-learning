from aiohttp import ClientSession
import asyncio
import time

API_URLS = [
    "http://localhost:8080/names/1",
    "http://localhost:8080/names/2",
] * 1000


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_all():
    async with ClientSession() as session:
        tasks = [fetch(session, url) for url in API_URLS]
        results = await asyncio.gather(*tasks)
        # print(results)


start_time = time.perf_counter()


asyncio.run(fetch_all())

end_time = time.perf_counter()
print(f"Duration: {round(end_time - start_time, 2)} seconds")
