# 将函数绑定到不同的名称
def hello():
    print("Hello World")

func = hello
func()

def fun(abs,x,y): # 将函数作为参数
    return abs(x)+abs(y)

print(fun(abs,10,-2))

# 将函数作为返回值
def outer():
    def inner(n):
        sum = 0
        for i in range(1,n):
            sum += i
        return sum
    return inner
inner = outer()
print(inner(10))