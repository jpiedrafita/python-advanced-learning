import asyncio
import time


class TimingEventLoop(asyncio.SelectorEventLoop):
    def run_until_complete(self, future):
        start_time = time.perf_counter()
        result = super().run_until_complete(future)
        end_time = time.perf_counter()
        print(f"Event loop execution time: {round(end_time - start_time, 2)} seconds")
        return result


class TimingEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self):
        return TimingEventLoop()
