import random,time,copy,sys

def quick_sort(data,left,right):
    if left < right:
        mid = partition(data,left,right)
        quick_sort(data,left,mid-1)
        quick_sort(data,mid+1,right)

def partition(data,left,right):
    tmp = data[left]
    while left < right:
        while left < right and data[right] >= tmp:
            right -= 1
        data[left] = data[right]
        while left < right and data[left] <= tmp:
            left += 1
        data[right] = data[left]
    data[left] = tmp
    return left

data = list(range(100000))
random.shuffle(data)
data1 =copy.deepcopy(data)
stime = time.time()
quick_sort(data,0,len(data)-1)
etime = time.time()
print("cost:",etime-stime)

stime = time.time()
data.sort()
etime = time.time()
print("cost:",etime-stime)

sys.setrecursionlimit(1000) # 设置递归限制