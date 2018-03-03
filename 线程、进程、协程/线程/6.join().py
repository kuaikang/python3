import threading
import time


def task(n):
    time.sleep(3)
    print("task", n)


def main():
    for i in range(3):
        t = threading.Thread(target=task, args=(i,))
        t.start()
        t.join()
    return "finish"


if __name__ == '__main__':
    result = main()
    print(result)
    print("main thread")