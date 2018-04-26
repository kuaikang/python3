from pymongo import MongoClient

if __name__ == '__main__':
    # 建立MongoDB数据库连接
    client = MongoClient('192.168.121.56', 27117)
    # 连接所需数据库,assignment为数据库名
    db = client.get_database('assignment')
    # 连接所用集合，也就是我们通常所说的表，test为表名
    table = "t_student_assignment_map_397718251448049664"
    if table in db.collection_names():
        col = db.get_collection(table)
    # print(col.find_one())
    # limit()方法用来读取指定数量的数据
    # skip()方法用来跳过指定数量的数据
    for item in col.find().skip(2).sort([("createTime", 1)]).limit(10):
        print(item)
    client.close()
