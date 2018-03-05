# 这节讲继承,经典类 ，新式类
# class People: 经典类
class People(object): # 新式类
    name = "people_name"
    def __init__(self,name,age):
        self.name = name
        self.age = age
        self.friends = []

    def talk(self):
        print("people can talk...",self.name)

class Relation():
    def get_friends(self,obj):
        print("%s is making friends with %s"%(self.name,obj.name))
        self.friends.append(obj) # 参数obj，这样obj的属性改变，self的friends属性也会改变

class Man(People,Relation): # 多继承
    def __init__(self,name,age,sex):# 对构造函数进行重构
        # People.__init__(self,name,age) # 经典类的写法
        super(Man,self).__init__(name,age) # 和上面一句作用一样，新式类的写法
        self.sex = sex

    def talk(self): # 重写了父类的方法
        People.talk(self) # 强行调用父类的方法
        print("man can talk...")

m = Man("tom",24,"man")
m1 = Man("jack",25,"man")
# m.talk()
# print(Man.name)
print(m.get_friends(m1))
m1.name = "update"
print(m.friends[0].name)