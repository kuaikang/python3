from common.mysql_util import mysql

sql = "select count(1) from t_res_{subject_key}_question;"


def get_count(subject_key):
    with mysql(db="topic_standard") as cur:
        cur.execute(sql.format(subject_key=subject_key))
        return cur.fetchone()


if __name__ == '__main__':
    keys = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", "dd", "sp"]
    total = 0
    for key in keys:
        num = get_count(key).get('count(1)')
        print(key, num)
        total += num
    print(total)
