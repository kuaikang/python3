# Python3 中有六个标准的数据类型：Number（数字）String（字符串）List（列表）Tuple（元组）Sets（集合）Dictionary（字典）
# type()不会认为子类是一种父类类型。isinstance()会认为子类是一种父类类型。
# 注意：在 Python2 中是没有布尔型的,它用数字0表示False,用1表示True
# Python3中,把True和False定义成关键字了,但它们的值还是1和0,它们可以和数字相加。
num1 = 10
print(num1, type(num1))
str = "Hello"
print(str, type(str))
li = (1, 2, 3, 4, "5")
print(li, type(li))
tup = [1, 2, 3, 4]
print(tup, type(tup))
s = set()  # 或 s = {"1","2"}
# 可以使用大括号 { } 或者 set() 函数创建集合，注意：创建一个空集合必须用 set() 而不是 { }，因为 { } 是用来创建一个空字典。
print(s, type(s))
dic = {"k1": "v1"}
print(dic, type(dic))
