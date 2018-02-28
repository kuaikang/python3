import random
# 选择排序,每一趟把最小的元素放到前面
def select_sort(li):
    for i in range(len(li)-1):
        min_index = i
        for j in range(i+1,len(li)):
            if li[j] < li[min_index]:
                min_index = j
        li[i],li[min_index] = li[min_index],li[i]

data = list(range(100))
random.shuffle(data) # 打乱列表中的元素
select_sort(data)
print(data)