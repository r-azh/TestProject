__author__ = 'R.Azh'

import asyncio
import time


@asyncio.coroutine
def sleep_coro(name, loop, seconds=1):
    future = loop.run_in_executor(None, time.sleep, seconds)
    print('[%s] coroutin will sleep for %d second(s)...' % (name, seconds))
    yield from future
    print('[%s] done' % name)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    tasks = [asyncio.Task(sleep_coro('Task_A', loop, 10)),
            asyncio.Task(sleep_coro('Task_B', loop)),
            asyncio.Task(sleep_coro('Task_C', loop))]

    loop.run_until_complete(asyncio.gather(*tasks))