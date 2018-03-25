import os, requests

if __name__ == '__main__':
    path = "E:/resource/历史/八年级/北师大版/下册/"
    dirs = os.listdir(path)
    print(dirs)
    count = 0
    for d in dirs:
        for root, dirs, files in os.walk(path + d):  # 遍历统计
            for each in files:
                size = os.path.getsize(path + d + "/" + each)/1024/1024
                if size > 3:
                    print(size)
                    print(d)
                count += 1
    print("数量",count)
