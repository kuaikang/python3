from threading import Timer
import time
count = 0


def loopfunc(msg,start_time):
    global count
    print (u'启动时刻：', start_time, ' 当前时刻：', time.time(), '消息 --> %s' % (msg))
    count += 1
    if count < 3:
        Timer(3, loopfunc, ('world %d' % (count), time.time())).start()

Timer(3, loopfunc, ('world %d' % (count), time.time())).start()