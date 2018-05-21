import math
import random

if __name__ == '__main__':
    print("取绝对值:", abs(-1))
    print("返回商和余数的元祖：", divmod(10, 3))
    print("开方：", pow(5, 2))
    print("保留2位小数：", round(123.456, 2))
    print("取整：", int(12.3), int(12.5))
    print("向下取整：", math.floor(-12.3))

    """random模块常用函数"""
    L = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("随机返回列表一个值：", random.choice(L))
    print("以列表形式随机返回多个值：", random.sample(L, 3))
    print("返回0-100之间任意整数", random.randint(0, 100))
