mod = __import__("lib.student") # python内部动态导入调用的
print(mod)

obj = mod.student.Student("tom")
print(obj.name)

'''下面这种是官方建议使用的'''
import importlib
stu = importlib.import_module("lib.student")
s = stu.Student("jack")
print(s.name)

assert type(s.name) is str # 验证数据类型，断言错误 AssertionError