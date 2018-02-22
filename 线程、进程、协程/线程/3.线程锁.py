import threading,time
num = 0
lock = threading.Lock() # 引入锁
def run():
    # lock.acquire() # 加锁
    global num
    num += 1
    # lock.release() # 释放锁

for i in range(100):
    threading.Thread(target=run,args=()).start()

print(num)