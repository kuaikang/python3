import os


if __name__ == '__main__':
    for i in range(9):
        print(i)
        os.system("python download_img.py sx")
        os.system("python download_img.py wl")
    print("finish")