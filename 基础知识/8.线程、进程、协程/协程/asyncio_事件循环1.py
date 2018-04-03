import asyncio


async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation(future))
    print(loop.is_running())  # False
    loop.run_until_complete(future)
    print(future.result())
    loop.close()
