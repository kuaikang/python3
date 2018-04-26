import time
import sys


def main():
    print("main start test 1")
    time.sleep(10)
    print("end")


if __name__ == '__main__':
    if sys.argv[1]:
        print(sys.argv[1])
    main()