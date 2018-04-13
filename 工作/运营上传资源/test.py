import os


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        L.append(dirs)
    return L


# os.path.splitext()函数将路径拆分为文件名+扩展名

if __name__ == '__main__':
    child_dirs = file_name("F:/冀人版3上科学PPT课件教案素材")
    for child in child_dirs:
        print(child)
        # print(os.listdir(child))
