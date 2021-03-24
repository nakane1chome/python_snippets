#!/bin/env python3

import asyncio


async def worker_task():
    print("Worker task starting, control-C to exit")
    try:
        while True:
            await asyncio.sleep(1.0)
            print("working...")
    except asyncio.CancelledError:
        print("Worker task cancelled..")


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(worker_task())
    print("Did we get here?")
finally:
    print("Cancel all tasks")
    for task in asyncio.Task.all_tasks():
         task.cancel()
    loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
    print("All tasks complete")
