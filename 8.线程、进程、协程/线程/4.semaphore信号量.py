import threading,time
sempahore = threading.BoundedSemaphore(5) # 添加一个计数器
def run(n):
    sempahore.acquire() # 计数器获得锁
    time.sleep(2)
    print("task --",n)
    sempahore.release() # 数器释放锁

for i in range(20):
    t = threading.Thread(target=run,args=(i,))
    t.start()