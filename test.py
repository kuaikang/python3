import pymysql


def get_db_spark():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host="123.206.227.74", user="root",
            password="exue2017", db="sit_exue_resource", port=3306,
            charset="utf8"
        )
        return db
    except Exception as e:
        print(e)


def main(subject_key):
    db = get_db_spark()
    cur = db.cursor()
    cur.execute(
        "SELECT tq.tag_id,tq.tag_name from t_res_{}_tag_question tq LEFT JOIN t_res_{}_tag t on tq.tag_id = t.tag_id WHERE  t.tag_name is null GROUP BY tq.tag_id".format(
            subject_key,subject_key))
    data = cur.fetchall()
    for d in data:
        sql = "INSERT INTO t_res_{}_tag (`tag_id`, `tag_name`, `tag_description`, `tag_url`) VALUES ('{}', '{}', NULL, NULL);"
        print(sql.format(subject_key, d[0], d[1]))
    cur.close()
    db.close()


if __name__ == '__main__':
    main('yw')
    main('sx')
    main('yy')
    main('ls')
    main('dl')
    main('sw')
    main('hx')
    main('wl')