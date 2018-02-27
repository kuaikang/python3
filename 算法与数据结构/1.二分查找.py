import time
# 列表查找


# 对有序列表进行二分查找
def bin_search(data_set,val):
    low = 0
    high = len(data_set)-1
    while low <= high:
        mid = (low+high) // 2
        if data_set[mid] == val:
            return mid
        elif data_set[mid] < val:
            low = mid + 1
        else:
            high = mid - 1
    return None

start_time = time.time()
data_set = [i for i in range(10000)]
bin_search(data_set,165)
end_time =time.time()
print("cost:",end_time-start_time)