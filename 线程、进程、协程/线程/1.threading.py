import threading,time


# 方法一：将要执行的方法作为参数传给Thread的构造方法
def task(n):
    print("task -- ",n)
    time.sleep(2)


for i in range(4):
    t = threading.Thread(target=task,args=(i,))
    t.start()


# 方法二：从Thread继承，并重写run()
class MyThread(threading.Thread):
    def __init__(self,arg):
        super(MyThread, self).__init__()  # 注意：一定要显式的调用父类的初始化函数。
        self.arg = arg

    def run(self):
        print("task -- ", self.arg)
        time.sleep(2)


for i in range(4):
    t = MyThread(i)
    t.start()
