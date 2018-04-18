import configparser

if __name__ == '__main__':
    cf = configparser.ConfigParser()
    cf.read("conf.ini")
    print(cf.sections())  # 获取所有读到的域,返回列表
    print(cf.options("test"))  # 获取某个域下的所有key,返回列表
    print(cf.items("test"))  # 获取某个域下的所有key,val对
    print(cf.get("test", "ip"))  # 获取某个域下的key对应的value值,返回字符串
    print(cf.has_section("abc"))  # 检测是否存在指定的域
