# 静态方法、类方法

class Dog(object):
    def __init__(self,name):
        self.name = name

    @staticmethod # 静态方法，可以通过类名或实例来调用
    def eat(self):
        print("%s eat %s"%(self.name,"包子"))
    @classmethod # 类方法，只能访问类变量
    def talk(self):
        print("talk ....")

d = Dog("中华田园犬")
# d.eat(d,"包子")
Dog.eat(d)