import threading,time
def task(n):
    print("task -- ",n)
    time.sleep(3)
    print("task",n,"done")

t = threading.Thread(target=task,args=("t1",))
t.setDaemon(True) # 设置为守护线程,要在start之前才起作用
t.start()

print("主进程结束") # 从打印结果可以知道运行要这里程序就结束了,没有等到线程的结束
