name = "全局变量"
def change_name1():
    print("change_name1() --->",name)

def change_name2():
    name = "局部变量"
    print("change_name2() --->",name) # 方法里优先访问局部变量

def change_name3():
    global name #
    name = "修改了全局变量name"
    print("change_name3() --->",name)

if __name__ == '__main__':
    change_name1()
    change_name2()
    change_name3()