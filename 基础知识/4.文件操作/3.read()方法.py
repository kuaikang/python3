import json

# print("read()".center(50, "-"))
# f = open("test.txt", "r", encoding="utf-8")
# print(f.read())  # 10表示从文件中读取的字节数.不填则表示读取所有
# f.close()
#
# print("readline()".center(50, "-"))
# f = open("test.txt", "r", encoding="utf-8")
# print(f.readline())
# print(f.readline())
# f.close()
#
# print("readlines()".center(50, "-"))
# f = open("test.txt", "r", encoding="utf-8")
# data = f.readlines()  # 得到的是一个列表,每行是一个元素
# print(data)
# f.close()
#
# f = open("test.txt", "r", encoding="utf-8")
# for line in f.readlines():
#     print(line.strip())
# f.close()

# 读取text文件中的json数据
f = open("test.txt", mode="r", encoding="utf8")
for line in f:
    print(type(line))
    data = json.loads(line.strip())
    print(type(data))
f.close()
