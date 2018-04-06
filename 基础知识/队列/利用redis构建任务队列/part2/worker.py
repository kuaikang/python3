import redis
from rq import Worker, Queue, Connection

listen = ['default']
conn = redis.from_url("redis//localhost:6379", password='123456')


def square_func(x):
    return x * x


if __name__ == '__main__':
    with Connection(conn):  # 建立连接
        worker = Worker(list(map(Queue, listen)))
        worker.work()
