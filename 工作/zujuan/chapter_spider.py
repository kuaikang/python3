import requests, threading


def get_chapters(url, unit_id):
    resp = requests.get(url % unit_id)
    resp.close()
    return resp.json()


def main(read_file, write_file):
    url = "http://www.zujuan.com/question/tree?id=%s&type=category&_=1521177223714"
    f = open(read_file, mode="r", encoding="utf8")
    f1 = open(write_file, mode="a", encoding="utf8")
    for line in f.readlines():  # ['7820', '第三组', '7751\n']
        line = line.split(",")
        json = get_chapters(url, line[0])
        for j in json:
            f1.write(j['id'] + "," + j["title"].strip() + "," + line[0] + "," + line[-1].strip())
            f1.write("\n")
    f.close()
    f1.close()


if __name__ == '__main__':
    # main("xx_unit.txt", "xx_chapter.txt")
    # main("cz_unit.txt", "cz_chapter.txt")
    main("gz_unit.txt", "gz_chapter.txt")