class People:
    name = "我是类变量，所有实例共享"

    def __init__(self, name, age, phone):  # 构造函数，在类被实例化的时候执行
        self.name = name  # 实例变量，为每个实例所独有
        self.__age = age  # 在变量前面加__，表明这是私有变量,可以通过方法访问私有变量
        self.phone = phone

    def get_age(self):  # 定义一个方法来访问私有变量
        return self.__age


p = People("tom", 23, "13912345678")  # 通过构造函数实例化了一个对象,参数个数要一致
print("name:", p.name, ",phone:", p.phone)
# print(p.age)  #通过实例.属性的方式访问私有变量是会报错的 AttributeError: 'People' object has no attribute 'age'
print(p.get_age())  # 通过调用方法取到私有变量

# 实例化时可以为实例赋予属性，还有在外面为实例添加属性
p.address = "苏州"
print(p.address)

# 可以删除实例的属性
del p.address
# print(p.address) #这时打印p的address属性会报错 AttributeError: 'People' object has no attribute 'address'

# 注意在类的内部，使用def关键字可以为类定义一个函数（方法），与一般函数定义不同，类方法必须包含参数self,且为第一个参数！
