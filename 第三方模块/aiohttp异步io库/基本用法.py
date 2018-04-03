import aiohttp
import asyncio


async def get_github():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://github.com") as r:
            return await r.text()


if __name__ == '__main__':
    tasks = [get_github()]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
