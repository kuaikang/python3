import arrow

if __name__ == '__main__':
    now = arrow.now()
    # 获取数据
    print(now.year, now.month, now.day, now.hour, now.minute, now.second, now.week)

    # arrow可以转化多种格式的时间
    print(arrow.get("2018-01-03"))
    print(arrow.get("2018.01.03"))
    print(arrow.get("2018/01/03"))
    print(arrow.get("01-03-2018", 'MM-DD-YYYY'))
    print(arrow.get("01-03-2018", 'DD-MM-YYYY'))
    print(arrow.get("1586782011"))