import re


def valid_name(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


def re_name(name):
    reg = re.compile(r'[\\/:*?_"=<>|!@#$%^&()（）,.;\r\n]+')
    valid = reg.findall(name)
    if valid:
        for v in valid:
            name = name.replace(v, '')
    return name


if __name__ == '__main__':
    print(valid_name('<>春/?'))
    print(re_name('132fsdf涨=_@#$%^&()（）'))
