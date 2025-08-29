import asyncio
import time


async def worker_task(name, duration):
    print(f"{name}: Starting (duration: {duration} seconds)")
    try:
        for i in range(duration):
            await asyncio.sleep(1)
            print(f"{name}: Progress {i+1}/{duration} seconds")
        print(f"{name}: Completed successfully")
    except asyncio.CancelledError:
        print(f"{name}: Cancelled")
        raise
    finally:
        print(f"{name}: Cleaning up resources")


async def create_task_group():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(worker_task(name="Call API", duration=1))
        tg.create_task(worker_task(name="Load from DB", duration=1))
        tg.create_task(worker_task(name="Read very large file", duration=3))
    print("All tasks are created")


async def timeout_with_taskgroup():
    task = asyncio.create_task(create_task_group())
    await asyncio.sleep(2)

    print(f"Task group timeout reached after 2 seconds")

    task.cancel()

    try:
        await task
    except asyncio.CancelledError:
        print("Task group was cancelled due to timeout")


async def main():
    start_time = time.perf_counter()

    await timeout_with_taskgroup()

    end_time = time.perf_counter()
    print(f"Duration: {round(end_time - start_time, 2)}")


if __name__ == "__main__":
    asyncio.run(main())
