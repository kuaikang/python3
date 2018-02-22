# 多态的特性是：一种接口，多种实现
class Animal(object):
    def __init__(self):
        pass
    @classmethod # 静态方法(类方法)
    def animal_talk(self,obj):
        obj.talk()

class Dog(Animal):
    def talk(self):
        print("汪汪...")

class Cat(Animal):
    def talk(self):
        print("瞄瞄...")

c = Cat()
# c.talk()
Animal.animal_talk(c)
d = Dog()
# d.talk()
Animal.animal_talk(d)