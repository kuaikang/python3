if __name__ == '__main__':
    L = [i for i in dir(str) if not i.startswith('__')]
    print(L)

    s = "HelloWorld"
    print("首字母大写,其余小写", s.capitalize())
    print("字符串变为小写：", s.lower(), s.casefold())
    # lower() 只对英文字母A-Z有效 casefold()适用于存在其他语言大小写的情况

    print("字符串的长度：", len("abc"))  # 返回字符串的长度
    print("ABC".casefold())  # 大写全部变小写
    print("大小写互换：", "AbCd".swapcase())
    print("abc".center(50, "-"))
    print("abc".encode())  # 将字符串编码成bytes格式

    print("abc".startswith("ab"))  # 判断字符串abc是否以"ab"开头
    print("abc".endswith("b"))  # 判断字符串是否以"b"结尾

    s1 = "abcdefg"
    print(s1.find("cdf"))  # 查找，找到返回其索引，找不到返回-1
    print(s1.index("cd"))  # 与上面作用相同，不过找不到会报错

    print("99".isdigit())  # 检测字符串是否只由数字组成

    print("这是分割线".center(50, "-"))

    str = "ab,cd,ef,gh"
    print(str.split(","))  # 分割字符串，返回一个列表
    print(str.count("d"))  # 统计字符串中某个子字符串的数量
