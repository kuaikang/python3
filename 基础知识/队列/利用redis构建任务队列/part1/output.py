from 基础知识.队列.利用redis构建任务队列.part1.redis_queue import RedisQueue
import time

q = RedisQueue('rq')
while True:
    result = q.get_nowait()
    if not result:
        break
    print("output.py: data {} out of queue {}".format(result, time.strftime("%c")))
    time.sleep(2)
