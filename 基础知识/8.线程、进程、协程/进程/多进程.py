from multiprocessing import Pool
import time


def task(n):
    time.sleep(2)
    print("this is task", n)


if __name__ == '__main__':
    p = Pool(5)
    for i in range(5):
        p.apply_async(task, args=(str(i)))  # 将任务放进进程池
    p.close()  # 调用join()之前必须先调用close(),调用close()方法后就不能添加新的任务
    p.join()  # 等待所有子进程执行完毕
    print("everything is done")
