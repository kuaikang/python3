import redis,time # redis是线程安全的
pool = redis.ConnectionPool(host="localhost",port="6379",db=0) # 创建连接池
r = redis.Redis(connection_pool=pool) # 从连接池中取连接对象
with r.pipeline() as pipe:
    while 1:
        #关注一个key
        pipe.watch('stock_count’)
        count = int(pipe.get('stock_count'))
        if count > 0:  # 有库存
            # 事务开始
            pipe.multi()
            pipe.set('stock_count', count - 1)
            # 事务结束
            pipe.execute()
            # 把命令推送过去
        break
        # 如果在watch后值被修改，在执行pipe.execute()的时候会报异常WatchError: Watched variable changed.