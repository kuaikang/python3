import time

print("当前时间戳为:",time.time())
localtime = time.localtime(time.time()) # 从返回浮点数的时间戳方式向时间元组转换
print("本地时间为:",localtime)
print(localtime[0]) # 年
print(localtime[1]) # 月
print(localtime[2]) # 日
print(localtime[3]) # 时
print(localtime[4]) # 分
print(localtime[5]) # 秒
print(localtime[6]) # 周几(0是周一)
print(localtime[7]) # 一年中的第几天