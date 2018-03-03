class Student(object):
    def __init__(self,name,score):
        self.name = name
        self.score = score
    def __str__(self): # 打印实例时会调用这个方法
        # return "<obj:%s>"%self.name
        return "name:%s,score:%s"%(self.name,self.score)

print(Student.__dict__) # 打印类中的所有属性
s = Student("tom",89)
print(s.__dict__) # 打印某个实例的所有属性
print(s)