import re


def check_name_valid(name):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid_name = reg.findall(name)
    if valid_name:
        for v in valid_name:
            name = name.replace(v, '')
    return name


if __name__ == '__main__':
    print(check_name_valid('<>春/?'))
