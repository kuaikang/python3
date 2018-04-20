import requests, re, json, threading


def get_units(categories, bookversion, nianji, chid, xd):
    url = "http://www.zujuan.com/question?categories=%s&bookversion=%s&nianji=%s&chid=%s&xd=%s"
    resp = requests.get(url % (categories, bookversion, nianji, chid, xd))
    pattern = re.compile("<script>.*?fetchTree(.*?)function.*?</script>", re.S)
    units = re.findall(pattern, resp.text)[0]
    resp.close()
    units = units[units.find("["):units.rfind("]") + 1]
    data = []
    for j in json.loads(units):
        data.append(j["id"] + "," + j["title"].strip() + "," + nianji)
    return data


def main(read_file, write_file, level):
    f = open(read_file, mode="r", encoding="utf8")
    f1 = open(write_file, mode="a", encoding="utf8")
    for line in f.readlines():  # ['政治思品', '9', '浙教版', '28414', '六年级下册（品德与社会）', '33161\n']
        line = line.split(",")
        data = get_units(line[-1].strip(), line[3], line[-1].strip(), line[1], level)
        for d in data:
            print(d)
            f1.write(d)
            f1.write("\n")
    f.close()
    f1.close()


if __name__ == '__main__':
    t1 = threading.Thread(target=main, args=("xx.txt", "xx_unit.txt", "1",))
    t2 = threading.Thread(target=main, args=("cz.txt", "cz_unit.txt", "2",))
    t3 = threading.Thread(target=main, args=("gz.txt", "gz_unit.txt", "3",))

    t3.start()