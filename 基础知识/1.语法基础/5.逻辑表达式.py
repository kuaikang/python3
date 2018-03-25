# 在Python中，真值为假的对象，包括False，None，数字0，空字符串以及空的容器类型。除此以外的任何对象均为真。
print("a=5", "and", False, "--->", "a=5" and False)
print("a=5", "or", False, "--->", "a=5" or False)
print("a=5", "and", True, "--->", "a=5" and True)
print("a=5", "or", True, "--->", "a=5" or True)

print("not False --> ", not False)
print("not 'a=5' --> ", not "a=5")
print("not 0 --> ", not 0)
print("not None --> ", not None)

# python采用短路原则返回结果,例如：a and b
# 假如a为真,则b的值决定表达式值,结果为b
# 假如a为假,则表达式的值就是a
