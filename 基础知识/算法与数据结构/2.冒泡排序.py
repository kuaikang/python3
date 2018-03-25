import random,time
def bubble_sort(list):
    for i in range(len(list)-1):
        for j in range(len(list)-i-1):
            if list[j] > list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]

# 优化版 如何执行一趟没有发生交换,则列表已经是有序,可以结束排序
def bubble_sort_perfect(list):
    for i in range(len(list)-1):
        exchange = False
        for j in range(len(list)-i-1):
            if list[j] > list[j+1]:
                list[j],list[j+1] = list[j+1],list[j]
                exchange = True
        if not exchange:
            return

data = list(range(3000))
random.shuffle(data) # 打乱列表中的元素
start_time = time.time()
bubble_sort(data)
end_time = time.time()
print("cost:",end_time-start_time)
# print(data)