import os


def main():
    path = "F:/img/wl_0424/tag"
    dirs = os.listdir(path)
    result = set()
    for d in dirs:
        q_path = os.path.join(path, d)
        data = os.listdir(q_path)
        for item in data:
            src_path = os.path.join(q_path, item)
            f = open(src_path, mode="rb")
            result.add(f.read())
            f.close()
    print(len(result))


if __name__ == '__main__':
    main()
