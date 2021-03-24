#!/bin/env python3

import asyncio

async def worker_task0(done=None):
    print("worker task0 starts")
    await asyncio.sleep(2.0)
    print("worker task0 done")
    if done:
        done.set_result(True)

async def worker_task1():
    print("worker task1 starts")
    await asyncio.sleep(1.0)
    print("worker task1 done")

print("########################################## Example 1.1")

print("Schedule each future")
loop = asyncio.get_event_loop()
done=asyncio.Future()
asyncio.ensure_future(worker_task0(done), loop=loop)
asyncio.ensure_future(worker_task1(), loop=loop)
loop.run_until_complete(done)

print("########################################## Example 1.2")

print("Wrap with gather")
loop.run_until_complete(    
    asyncio.gather(
        worker_task0(),
        worker_task1()))

print("########################################## Example 2")

def _background_work(complete_callback):
    loop = asyncio.get_event_loop()
    loop.call_later(3.0, complete_callback)

def return_future_and_perform_background_work():
    print("return_future_and_perform_background_work starts")
    complete = asyncio.Future()
    _background_work(complete_callback=lambda: complete.set_result(True))
    print("return_future_and_perform_background_work returns")
    return complete

async def another_background_task():
    print("another_background_task starts")
    await asyncio.sleep(2.0)
    print("another_background_task returns")

async def do_multple_background_tasks():
    print("do_multple_background_tasks starts")
    task1_done = return_future_and_perform_background_work()
    await asyncio.gather(another_background_task(), task1_done)
    print("do_multple_background_tasks returns")

loop.run_until_complete(do_multple_background_tasks())
