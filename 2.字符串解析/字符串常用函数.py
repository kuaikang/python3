print("字符串的长度：", len("abc"))  # 返回字符串的长度
print("首字母大写:", "abc".capitalize())
print("ABC".casefold())  # 大写全部变小写
print("大小写互换：", "AbCd".swapcase())
print("abc".center(50, "-"))
print("abc".encode())  # 将字符串编码成bytes格式

print("abc".startswith("ab"))  # 判断字符串abc是否以"ab"开头
print("abc".endswith("b"))  # 判断字符串是否以"b"结尾

str = "abcdefg"
print(str.find("cd"))  # 查找，找到返回其索引，找不到返回-1
print(str.index("cd"))  # 与上面作用相同，不过找不到会报错

print("99".isdigit())  # 检测字符串是否只由数字组成

print("这是分割线".center(50, "-"))

str = "ab,cd,ef,gh"
print(str.split(","))  # 分割字符串，返回一个列表
print(str.count("d"))  # 统计字符串中某个子字符串的数量

'''连接字符串'''
list = ["tom", "jom", "lily"]
print(":".join(list))  # 把列表每个元素连接成字符串，用：分割

# 解决\u开头的字符串转中文方法
# python3的解决办法：字符串.encode('utf-8').decode('unicode_escape')
# python2：字符串.decode('unicode_escape')
