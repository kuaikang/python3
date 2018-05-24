if __name__ == '__main__':
    li = [1, "2", 3, 4]  # list列表里面可以放任何类型
    li.append(5)  # 增加元素到列表最后
    print("li.append(5)  -->", li)
    li.insert(1, 6)  # 添加元素到指定索引,第一个参数表示索引,第二个参数表示值
    print("li.insert(1,6)--> ", li)

    li.remove(3)  # 删除元素,3表示值
    print("li.remove(3) -->", li)
    del li[0]  # 删除列表索引为0的值
    print("del li[0] -->", li)
    li.pop()  # 默认删除最后一个值,填了索引则删除指定值
    print("li.pop()  --> ", li)

    li[0] = "6"  # 修改
    print("li[0]='6' --> ", li)

    # 获取具体某个值,用索引来访问,-1表示最后一个,-2表示倒数第二
    print("-------------------------")
    # 获取某些值,可以用截取的方式
    li = [i for i in range(10)]
    print(li)
    print("li[2:] --> ", li[2:])
    print("li[2:9]--> ", li[2:9])
    print("li[2::2]--> ", li[2::2])

    print()
    print("其他函数".center(50, "-"))
    print("列表元素个数:", len(li))
    print("列表元素最大值:", max(li))
    print("列表元素最小值:", min(li))
    li.reverse()  # 列表倒序
    print(li)

    li = [2, 6, 8, 3, 4, 7]
    print("原来的列表:", li)
    li.sort(reverse=True)  # reverse默认False,表示从小到大排序,为True时表示从大到小排序
    print("从大到小排序后列表:", li)
    li.sort()
    print("从小到大排序后列表:", li)


