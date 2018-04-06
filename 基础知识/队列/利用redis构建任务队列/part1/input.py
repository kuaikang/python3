from 基础知识.队列.利用redis构建任务队列.part1.redis_queue import RedisQueue
import time

q = RedisQueue('rq')  # 新建队列名为rq
for i in range(5):
    q.put(i)
    print("input.py: data {} enqueue {}".format(i, time.strftime("%c")))
    time.sleep(1)
