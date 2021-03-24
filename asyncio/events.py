#!/bin/env python3

import asyncio
import collections

class Consumer:
    def __init__(self):
        self.event = asyncio.Event()
        self.datas = collections.deque()

    def callback_from_producer(self, data):
        self.datas.append(data)
        self.event.set()

    async def pop(self):
        if len(self.datas)==0:
            await self.event.wait()
            self.event.clear()
        return self.datas.popleft()

async def worker_task(consumer):
    while True:
        data = await consumer.pop()
        print(f"Got {data}")
        if data == "data 3":
            return

consumer = Consumer()

loop = asyncio.get_event_loop()
loop.call_later(1.0, lambda: consumer.callback_from_producer("data 1"))
loop.call_later(2.0, lambda: consumer.callback_from_producer("data 2"))
loop.call_later(3.0, lambda: consumer.callback_from_producer("data 3"))

loop.run_until_complete(worker_task(consumer))

