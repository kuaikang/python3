from DBUtils.PooledDB import PooledDB
import pymysql

mysqlInfo = {
    "host": '123.206.227.74',
    "user": 'root',
    "password": 'exue2017',
    "db": 'sit_exue_resource',
    "port": 3306,
    "charset": 'utf8'
}


class OPMysql(object):
    __pool = None

    def __init__(self):
        # 构造函数，创建数据库连接、游标
        self.coon = OPMysql.get_mysql_conn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def get_mysql_conn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20, host=mysqlInfo['host'],
                              user=mysqlInfo['user'], passwd=mysqlInfo['password'], db=mysqlInfo['db'],
                              port=mysqlInfo['port'], charset=mysqlInfo['charset'])
        return __pool.connection()

    # 插入\更新\删除sql
    def op_insert(self, sql):
        print('op_insert', sql)
        insert_num = self.cur.execute(sql)
        self.coon.commit()
        return insert_num

    # 查询
    def op_select_one(self, sql):
        print('op_select_one', sql)
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchone()  # 返回结果为字典
        return select_res

    # 查询
    def op_select_all(self, sql):
        print('op_select_all', sql)
        self.cur.execute(sql)  # 执行sql
        select_res = self.cur.fetchall()  # 返回结果为字典
        return select_res

    # 释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()


if __name__ == '__main__':
    opm = OPMysql()
    sql = "select * from t_res_book limit 1"
    res = opm.op_select_one(sql)
    print(res)
    opm.dispose()
