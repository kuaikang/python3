s = set()  # 定义空的集合,set集合不能重复，无序
print(type(s))

# 添加
s.add("tom")  # 是把要传入的元素做为一个整个添加到集合中
s.update("tom")  # 是把要传入的元素拆分，做为个体传入到集合中,实际上是添加3个元素
print(s)

# 删除
s_pop = s.pop()  # 删除集合最后一个元素,因为集合是无序的,所以这种删除是随机的,不适用
print("随机删除的元素:", s_pop)
# s.remove("tom")  # 标准删除
print(s)

s1 = {1, 2, 3, 4, 5}
s2 = {3, 5, 6}
print(s1 - s2)

