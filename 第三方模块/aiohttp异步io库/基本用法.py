import aiohttp
import asyncio
import time


async def get_github():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.zujuan.com/question/detail-1296078.shtml") as r:
            return await r.text()


if __name__ == '__main__':
    s = time.time()
    tasks = []
    for i in range(20):
        tasks.append(get_github())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print(time.time()-s)
