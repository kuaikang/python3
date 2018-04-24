import sys


class test(object):
    def __init__(self, name):
        self.name = name


class test2(object):
    """__slots限制该class能添加的属性"""
    __slots__ = ["name"]

    def __init__(self, name):
        self.name = name


a = test('alex')
b = test2('lilei')

print(sys.getsizeof(a))

print(sys.getsizeof(b))
