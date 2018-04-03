import asyncio
import datetime


def display_date(num, loop):
    end_time = loop.time() + 10.0
    while True:
        print("Loop: {} Time: {}".format(num, datetime.datetime.now()))
        if (loop.time() + 1.0) > end_time:
            break
        yield from asyncio.sleep(2)  # 阻塞直到协程sleep(2)返回结果


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    print(loop.time())
    tasks = [display_date(1, loop), display_date(2, loop), display_date(3, loop)]
    loop.run_until_complete(asyncio.gather(*tasks))  # "阻塞"直到所有的tasks完成
    loop.close()
