class Person(object): # 类如果没有指定父类,那么它的父类就是object
    # 必须在__init__(self,…)方法内(注意：双下划线)初始化实例，第一个参数必须为self
    # 如需动态添加属性，可用 **kwargs
    def __init__(self,name,gender,birth,**kwargs):
        self.name = name
        self.gender = gender
        self.birth = birth
        for k,v in kwargs.items():
            setattr(self,k,v)

