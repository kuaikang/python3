class A(object): # 新式类
    def __init__(self):
        print("AAA")

class B(A):
    def __init__(self):
        print("BBB")

class C(A):
    def __init__(self):
        print("CCC")

class D(B,C):
    def __init__(self):
        print("DDD")

d = D()
# 新式类 广度优先
# 实例化时首先找D的构造函数，D没有就找B的，B也没有就找C的，C没有找A
# python3 经典类和新式类统一按广度优先来继承
# python2 经典类按深度优先继承，新式类按广度优先来继承

''' 经典类 深度优先 '''
# class A:
#     def __init__(self):
#         pass