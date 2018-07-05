import pymysql
import json
import uuid


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host='192.168.121.159', port=42578, user='root', password='D8VsaJj=>?Ev1165', db='uat_exue_resource',
            charset='utf8'
        )
        return db
    except Exception as e:
        print(e)


db = get_db()
cur = db.cursor(pymysql.cursors.DictCursor)

insert = "insert into t_res_{subject}_question_tag values('{id}','{tag_id}','{question_uuid}',NOW());"


def uuid_get():
    return str(uuid.uuid4()).replace("-", "")


def main(file, subject):
    f_write = open("%s_sql.txt" % subject, mode="a", encoding="utf8")
    with open(file, mode="r", encoding="utf8") as f:
        for line in f.readlines():
            line = json.loads(line)
            for key in line.keys():
                cur.execute("select * from t_res_%s_tag_question where tag_id = '%s'" % (subject, key))
                for item in cur.fetchall():
                    # print(item.get('question_uuid'))
                    for d in line.get(key):
                        for k in d.keys():
                            f_write.write(insert.format(subject=subject, id=uuid_get(), tag_id=k,
                                                        question_uuid=item.get('question_uuid')))
                            f_write.write("\n")
                            # cur.execute(insert.format(subject=subject, id=uuid_get(), tag_id=k,
                            #                           question_uuid=item.get('question_uuid')))
                    # db.commit()
    f_write.close()


if __name__ == '__main__':
    main('yw_map.txt', 'yw')
    main('yy_map.txt', 'yy')
