import random, time


def decorator(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        stime = time.time()
        return func(*args, **kwargs)
        etime = time.time()
        print("cost", etime - stime)

    return wrapper


def bubble_sort(li):
    for i in range(len(li) - 1):
        for j in range(len(li) - i - 1):
            if li[j] > li[j + 1]:
                li[j], li[j + 1] = li[j + 1], li[j]


li = list(range(1000))
random.shuffle(li)  # 打乱列表
decorator(bubble_sort(li))
