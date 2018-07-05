from common.mysql_util import get_db
import pymysql

db = get_db(db="uat_exue_resource")
cur = db.cursor(pymysql.cursors.DictCursor)


def main():
    result = []
    with open("a.txt", mode="r", encoding="utf8") as f:
        for line in f.readlines():
            if line.startswith("SELECT"):
                cur.execute(line.strip())
                for d in cur.fetchall():
                    result.append(d.get('book_id'))
    print(result)


if __name__ == '__main__':
    main()
