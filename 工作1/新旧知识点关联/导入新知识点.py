import pymysql
from common.excel_util import read_excel
import uuid


def get_db():
    # 打开数据库连接
    try:
        db = pymysql.connect(
            host='221.224.143.68', port=42580, user='root', password='root', db='topic_standard_test', charset='utf8'
        )
        return db
    except Exception as e:
        print(e)


db = get_db()
cur = db.cursor()
db.autocommit(True)

insert = """
          INSERT into t_res_tag(id,tag_name,parent_id,subject_id,subject_Key,subject_Name,period_id,level,is_easy,creator,
          create_time,status,is_delete,sort_num) VALUES
        ('{id}','{tagName}','{parentId}','{subjectId}','{subjectKey}','{subjectName}','{periodId}',
          '{level}',{isEasy},'{creator}',NOW(),'0','0',{sortNum})
        """


def main(subjectId, subjectKey, subjectName, periodId, file):
    num = 1
    cur.execute("select max(sort_num) from t_res_tag")
    data = cur.fetchone()
    print(data)
    if data[0]:
        num = data[0]

    data = read_excel("C:/Users/开发/Desktop/知识点/{file}".format(file=file))
    dict = {}
    for line in data[1:]:
        isEasy = "null"
        if line[8]:
            isEasy = "'" + str(int(line[8])) + "'"

        if line[0]:
            dict[0] = uuid_get()
            cur.execute(
                insert.format(id=dict[0], tagName=line[0], parentId='0', subjectId=subjectId, subjectKey=subjectKey,
                              subjectName=subjectName, periodId=periodId, level='1',
                              isEasy=isEasy, creator="1", sortNum=num))
            num += 1
        for i in range(1, 8):
            if line[i]:
                dict[i] = uuid_get()
                cur.execute(
                    insert.format(id=dict[i], tagName=line[i], parentId=dict[i - 1], subjectId=subjectId,
                                  subjectKey=subjectKey,
                                  subjectName=subjectName, periodId=periodId, level=i+1,
                                  isEasy=isEasy, creator="1", sortNum=num))
                num += 1


def uuid_get():
    return str(uuid.uuid4()).replace("-", "")


if __name__ == '__main__':
    main("010", "yw", "语文", "1", "小学语文知识点体系.xls")
    main("010", "yw", "语文", "2", "初中语文知识点体系.xls")

    main("020", "sx", "数学", "1", "小学数学知识点体系a.xlsx")
    main("020", "sx", "数学", "2", "初中数学知识点体系a.xlsx")

    main("030", "yy", "英语", "1", "小学英语知识体系11（新加注）.xls")
    main("030", "yy", "英语", "2", "初中英语知识体系22（新加注）.xls")

    cur.close()
    db.close()