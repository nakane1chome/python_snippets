#!/bin/env python3

import asyncio
import signal

async def worker_task(program_complete):
    print("worker task starting, control-c to exit")
    while not program_complete.done():
          await asyncio.sleep(1)
          print("working...")

async def cleanup_task(program_complete):
    status = await program_complete
    print("cleanup...")
    return

program_complete = asyncio.Future()
loop = asyncio.get_event_loop()
loop.add_signal_handler(signal.SIGINT, lambda: program_complete.set_result(True))
# Schedule a 'task'
asyncio.ensure_future(worker_task(program_complete), loop=loop)
# Keep the loop running with worker and cleanup until signal is processed and cleaned up.
loop.run_until_complete(cleanup_task(program_complete))
