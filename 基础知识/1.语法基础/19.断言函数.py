# python assert断言是声明其布尔值必须为真的判定，如果发生异常就说明表达示为假。
# 可以理解assert断言语句为raise-if-not，用来测试表示式，其返回值为假，就会触发异常。


if __name__ == '__main__':
    try:
        assert 1 == 2
    except AssertionError:
        print("assert error")
