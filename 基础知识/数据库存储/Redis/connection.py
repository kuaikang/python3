import pymysql

def get_list():
    with open("语文湘教版二上（标准版）.txt",mode="r",encoding="utf-8") as f:
        data = f.read()
        print(data)

def insert_many(list):
    # 打开数据库连接
    db = pymysql.connect(host="192.168.0.168", port=3306, user="root", passwd='001233', db="kuaik", charset="utf8")
    # 使用cursor()方法获取游标对象
    cursor = db.cursor()
    # 使用预处理语句创建表
    try:
        # 执行sql
        sql = "INSERT INTO resource (`id`, `subject`, `publish`, `version`, `grade`, `material`) VALUES (%s,%S,%S,%S,%S,%S)"
        cursor.execute(sql,list)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误
        db.rollback()
    # data1=cursor.fetchone()
    # print("DB version is : %s" %data1)
    # 关闭连接
    db.close()

if __name__ == '__main__':
    print(type(get_list()))