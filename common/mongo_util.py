from pymongo import MongoClient
import time
import datetime


class mongo_operate(object):
    """mongoDB操作,结束之后要释放资源"""

    def __init__(self, host='localhost', post=27017, user='news', password='test123', db='newscenter'):
        self.client = MongoClient(host, post)
        self.db = self.client[db]
        self.db.authenticate(user, password)

    def insert(self, data):
        self.db.chapters.save(data)

    def find(self):
        return self.db.question.find()

    def release(self):
        self.client.close()


if __name__ == '__main__':
    op = mongo_operate()
    start_time = time.time()
    op.release()
    print(datetime.datetime.now())