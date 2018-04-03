import asyncio


async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')


def got_result(future):
    print(future.result())
    loop.stop()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(slow_operation(future))
    future.add_done_callback(got_result)
    try:
        loop.run_forever()
    finally:
        loop.close()

# run_forever相比run_until_complete的优势是添加了一个add_done_callback,
# 可以让我们在task(future)完成的时候调用相应的方法进行后续处理
