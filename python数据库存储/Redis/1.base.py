import redis,time # redis是线程安全的
pool = redis.ConnectionPool(host="localhost",port="6379",db=0) # 创建连接池
r = redis.Redis(connection_pool=pool) # 从连接池中取连接对象

r.set("name1","张三")
print(r.get("name1").decode())

# 默认pipeline执行的命令可以保证执行的原子性,有错误就回滚,可以通过transaction=False来禁用这个特性
pipe = r.pipeline(transaction=False) # 管道pipeline的意思先把要执行的命令存储起来,然后调用execute方法执行
pipe.set("name2","lucy") #
time.sleep(10)
pipe.set("name3","lily")
# 这时name2还没有存储到redis中,执行exxcute方法后才会保存到redis
pipe.execute()

# 也可以链式调用
# pipe.set("name4","jack").set("name5","bob").execute()


