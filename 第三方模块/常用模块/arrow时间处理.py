import arrow

if __name__ == '__main__':
    now = arrow.now()
    # 获取数据
    print(now.year, now.month, now.day, now.hour, now.minute, now.second, now.week)
    print(now.timestamp)  # 时间戳,精确到秒
    print(now.format('YYYY-MM-DD HH:mm:ss'))  # 格式化时间
