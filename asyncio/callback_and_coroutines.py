#!/bin/env python3

import asyncio

async def _blocking_replaced_by_await():
    await asyncio.sleep(1.0)

def _blocking_replaced_by_callback(complete_callback):
    loop = asyncio.get_event_loop()
    loop.call_later(1.0, complete_callback)

# Async/await
async def hello0():
    print ("Hello0: Enter")
    await _blocking_replaced_by_await()
    print ("Hello0: Complete")

# Future implementaion with no async/await keywords
def hello1():
    print ("Hello1: Enter")
    complete = asyncio.Future()
    def _my_callback():
        try:
            complete.set_result(True)
            print ("Hello1: Complete")
        except e:
            complete.set_exception(e)
    _blocking_replaced_by_callback(complete_callback=_my_callback)
    print ("Hello1: Exit")
    return complete


print ("Start")
loop = asyncio.get_event_loop()
# Both implementations should produce the same result
loop.run_until_complete(hello0())
loop.run_until_complete(hello1())
print ("End")

