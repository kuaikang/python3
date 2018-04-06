from rq import Queue
from rq.job import Job
from 基础知识.队列.利用redis构建任务队列.part2.worker import square_func, conn
import time

q = Queue(connection=conn)

job = q.enqueue_call(square_func, args=(5,), result_ttl=5000)  # 保存结果5000s
job_id = job.get_id()
print(job_id)

result = Job.fetch(job_id, connection=conn)
print(result.is_finished)

time.sleep(2)

result2 = Job.fetch(job_id, connection=conn)
print(result2.is_finished)
