class Teacher(object):
    def __init__(self,name):
        self.name = name
    def teach(self):
        print("teacher can teach student..")

def cook(self):
    print("%s is cooking..."%self.name)

t = Teacher("jon")
attr = input(">>:").strip()
if hasattr(t,attr): # 判断对象t中是否有方法fun
    # func = getattr(t,attr)
    # func(t)
    delattr(t,attr)
    print(t.name)
else:
    # setattr(t,fun,cook) # 动态为类添加方法
    # t.cook(t)
    setattr(t,attr,22)
    print(getattr(t,attr))

