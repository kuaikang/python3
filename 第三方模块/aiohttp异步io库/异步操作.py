import asyncio
import time
import requests


def ret():
    resp = requests.get("http://www.zujuan.com/question/detail-1296078.shtml")
    return resp.status_code


async def get_text():
    try:
        loop = asyncio.get_event_loop()
        # 主要在这
        resp = await loop.run_in_executor(None, ret)
        print(resp)
    except Exception:
        return None
    return resp

s =time.time()
tasks = []
for i in range(100):
    tasks.append(get_text())
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
print(time.time()-s)
if __name__ == '__main__':
    s = time.time()
    # for i in range(100):
    #     resp = requests.get("http://www.zujuan.com/question/detail-1296078.shtml")
    #     print(resp.status_code)
    # print(time.time()-s)