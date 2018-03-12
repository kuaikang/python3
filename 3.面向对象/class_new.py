# python类的起源是type，类是由type类实例化产生
def func(self):
    # print("%s is study very hard"%self.name)
    print("hello")


def __init__(self, name):
    self.name = name


''' 创建类的第二种方式 '''
Foo = type("Foo", (object,), {"talk": func, "__init__": __init__})
f = Foo("tom")
print(f.talk())
