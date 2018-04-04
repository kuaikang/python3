import asyncio


# 定义一个协程
async def do_some_work():
    await asyncio.sleep(3)  # asyncio.sleep也是一个协程


if __name__ == '__main__':
    print(asyncio.iscoroutinefunction(do_some_work))
