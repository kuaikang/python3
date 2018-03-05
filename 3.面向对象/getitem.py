class Foo(object):
    def __init__(self):
        self.data = {}

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key)

    def __delitem__(self, key):
        self.data.pop(key)

f = Foo()
f["id"] = "1"
str = f.__getitem__("id")
print(str)