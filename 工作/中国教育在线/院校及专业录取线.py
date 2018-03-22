if __name__ == '__main__':
    f = open("province.txt", mode="r", encoding="utf8")
    lines = f.readlines()
    for i in range(len(lines)):
        print(lines[i])