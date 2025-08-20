import asyncio
import time
from aiohttp import ClientSession
from custom_event_loop import TimingEventLoopPolicy

API_URLS = [
    "http://localhost:8080/names/1",
    "http://localhost:8080/names/2",
] * 1000  # simula carga de 2000 peticiones


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_all():
    start_time = time.perf_counter()

    async with ClientSession() as session:
        tasks = [fetch(session, url) for url in API_URLS]
        results = await asyncio.gather(*tasks)
        # print(results)

    end_time = time.perf_counter()
    print(f"Duration: {round(end_time - start_time, 2)}")


asyncio.set_event_loop_policy(TimingEventLoopPolicy())
asyncio.run(fetch_all())
