import asyncio
import datetime


async def display_date(num, loop):
    end_time = loop.time() + 10.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) > end_time:
            break
        await asyncio.sleep(2)  # 等同于yield from


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  # 获取一个event_loop 消息循环对象
    tasks = [display_date(1, loop), display_date(2, loop)]
    loop.run_until_complete(asyncio.gather(*tasks))  # "阻塞"直到所有的tasks完成
    loop.close()
