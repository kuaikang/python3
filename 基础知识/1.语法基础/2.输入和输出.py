print("Hello World")
print("Hello", "World")  # 遇到逗号会输出一个空格
print("100 + 200 =", 100 + 200)

print("Hello %s" % "World")
print("name:%s,age:%s" % ("Tom", 12))

# 格式化输出字符串
print("name:{},age:{}".format("Tom", 13))
print("name:{0},age:{1}".format("Tom", 14))
print("name:{name},age:{age}".format(name="Tom", age=15))
print("name:{name},age:{age}".format_map({"name": "Tom", "age": "16"}))

# 输入
name = input("please input your name:")
print("Hello", name)
