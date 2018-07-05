import copy

if __name__ == '__main__':
    a = [1, 2, 3, 4, ['a', 'b']]

    # 直接赋值,相当于把a的引用赋予b
    b = a
    print(b)
    a[0] = 2
    print(b)

    # 浅拷贝,拷贝父对象,不会拷贝对象的内部的子对象,把a复制了一份,但是其中最后一个元素还是指向同一个引用
    c = a.copy()
    print("浅拷贝得到c------>", c)
    a[-1].append('c')
    print(c)

    # 深拷贝,完全拷贝了父对象及其子对象,修改a并不会改变d
    d = copy.deepcopy(a)
    print(a, d)
    a[-1].append('d')
    print(a, d)

