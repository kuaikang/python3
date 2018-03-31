import asyncio
from aiohttp import ClientSession


async def hello():
    async with ClientSession() as session:
        async with session.get("http://httpbin.org/headers") as response:
            response = await response.read()
            print(dir(response))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(hello())

# 你使用async以及await关键字将函数异步化。在hello()中实际上有两个异步操作：首先异步获取相应，然后异步读取响应的内容。
# aiohttp推荐使用ClientSession作为主要的接口发起请求。ClientSession允许在多个请求之间保存cookie以及相关对象信息。
# Session(会话)在使用完毕之后需要关闭，关闭Session是另一个异步操作，所以每次你都需要使用async with关键字。
# 一旦你建立了客户端session，你可以用它发起请求。这里是又一个异步操作的开始。上下文管理器的with语句可以保证在处理session的时候，总是能正确的关闭它。
# 要让你的程序正常的跑起来，你需要将他们加入事件循环中。所以你需要创建一个asyncio loop的实例， 然后将任务加入其中。
# 看起来有些困难，但是只要你花点时间进行思考与理解，就会有所体会，其实并没有那么复杂。
