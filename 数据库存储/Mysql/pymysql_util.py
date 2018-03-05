import pymysql


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="localhost", user="root",
        password="123456", db="kuaik", port=3306,
        charset="utf8"
    )
    return db


def find_one(db, sql):
    try:
        # 使用cursor()方法获取操作游标
        cur = db.cursor()
        cur.execute(sql)
        results = cur.fetchone()
        return results
    except Exception:
        print("查询失败 sql-->", sql)
    finally:
        db.close()


def find_all(db, sql):
    try:
        cur = db.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        return results
    except Exception:
        print("查询失败 sql-->", sql)
    finally:
        db.close()


def find_many(db, sql, size=10):
    try:
        db = get_db()
        cur = db.cursor()
        cur.execute(sql)
        results = cur.fetchmany(size)
        return results
    except Exception:
        print("查询失败 sql-->", sql)
    finally:
        db.close()


def insert_one(db, sql):
    try:
        db = get_db()
        cur = db.cursor()
        result = cur.execute(sql)
        db.commit()
        return result  # 成功返回1
    except Exception:
        print("添加失败 sql-->", sql)
        db.rollback()  # 回滚
    finally:
        db.close()


def insert_many(db, sql, data):
    try:
        # 使用cursor()方法获取操作游标
        db = get_db()
        cur = db.cursor()
        result = cur.executemany(sql, data)
        db.commit()
        return result  # 成功返回1
    except Exception:
        print("添加失败 sql-->", sql)
        db.rollback()  # 回滚
    finally:
        db.close()


def update(db, sql, data):
    try:
        # 使用cursor()方法获取操作游标
        db = get_db()
        cur = db.cursor()
        cur.execute(sql % data)
        db.commit()
    except Exception:
        print("更新失败 sql-->", sql % data)
        db.rollback()  # 回滚
    finally:
        db.close()


def delete(db, sql, data):
    try:
        # 使用cursor()方法获取操作游标
        db = get_db()
        cur = db.cursor()
        cur.execute(sql % data)
        db.commit()
    except Exception:
        print("删除失败 sql-->", sql % data)
        db.rollback()  # 回滚
    finally:
        db.close()


if __name__ == '__main__':
    db = get_db()
    # s = find_one(db,"select * from student")
    # s = find_all(db,"select * from student limit 1")
    # s = find_many(db,"select * from student")
    # print(s)
    # res = insert_one(db,"INSERT INTO `kuaik`.`student` (`id`, `name`, `age`) VALUES ('102', 'Hello', '23')")
    # print(res)

    # data = (("103","tom","24"),("104","tom","24"))
    # data = [["105","tom","24"],["106","tom","24"]] # 2种格式都可以
    # res = insert_many(db,"INSERT INTO `kuaik`.`student` (`id`, `name`, `age`) VALUES (%s,%s,%s)",data)
    # print(res)

    # update(db,"update student set name = '%s' where id = %d",("9999",101))

    delete(db, "delete from student where id = %d", (101))
