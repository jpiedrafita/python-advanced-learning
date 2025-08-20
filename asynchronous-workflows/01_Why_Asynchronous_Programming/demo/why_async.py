import asyncio
import time


async def call_api():
    print("Calling API...")
    await asyncio.sleep(1)
    print("API response received.")


async def main():
    start_time = time.perf_counter()

    task = asyncio.create_task(call_api())  # start
    await call_api()  # start + finish
    await task  # finish

    end_time = time.perf_counter()
    print(f"Duration: {round(end_time - start_time, 3)} seconds")


asyncio.run(main())
