# Python的元组与列表类似,不同之处在于元组的元素不能修改
# 元组使用小括号,列表使用方括号
# 元组中只包含一个元素时,需要在元素后面添加逗号

if __name__ == '__main__':
    tup = ("tom", "jack", "lucy", "lily")
    print(tup[0], tup[1], tup[2])  # 通过索引获取值
    print(tup[1:], "\n", tup[::2])  # 元组的截取和列表是一样的

    print([i for i in dir(tuple) if not i.startswith('__')])
    print(tup.count("tom"))  # 统计元素数量
    print(tup.index("1"))  # 查找某元素索引位置,不存在会报错

    # tup[0] = "123" 修改索引为0的值,这样是错误的

    # 元组中的元素值是不允许删除的，但我们可以使用del语句来删除整个元组，如下实例:
    del tup
