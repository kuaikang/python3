import queue
import threading
import requests
from bs4 import BeautifulSoup

hosts = ["http://yahoo.com", "http://taobao.com", "http://apple.com",
         "http://ibm.com", "http://www.amazon.cn"]

host_queue = queue.Queue()  # 存放网址的队列
html_queue = queue.Queue()  # 存放网址页面的队列


class ThreadUrl(threading.Thread):
    def __init__(self, host_queue, html_queue):
        threading.Thread.__init__(self)
        self.host_queue = host_queue
        self.html_queue = html_queue

    def run(self):
        while True:
            host = self.host_queue.get()
            resp = requests.get(host)
            self.html_queue.put(resp.text)
            self.host_queue.task_done()  # 调用该方法,从队列中删除一个元素


class ThreadHtml(threading.Thread):
    def __init__(self, html_queue):
        threading.Thread.__init__(self)
        self.html_queue = html_queue

    def run(self):
        while True:
            html = self.html_queue.get()
            soup = BeautifulSoup(html)  # 从源代码中搜索title标签的内容
            print(soup.findAll(['title']))
            self.html_queue.task_done()


def main():
    for host in hosts:
        host_queue.put(host)

    t = ThreadUrl(host_queue, html_queue)
    t.start()
    t1 = ThreadHtml(html_queue)
    t1.start()


if __name__ == '__main__':
    main()
