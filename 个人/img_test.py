from common.mysql_util import mysql

f = open("F:/img/wl_0424/6965285/1e637455511b4907be0bad095398a832.png", mode="rb")
data = {
    f.read(): "E"
}
f.close()


def update():
    update = "UPDATE t_res_wl_question set answer = '{answer}' where uuid = '{uuid}';"
    with mysql(db="zujuan_spark_test") as cur:
        cur.execute("SELECT * from t_res_wl_question WHERE answer is null or answer = '';")
        for item in cur.fetchall():
            try:
                f = open(item.get('answer_url'), mode="rb")
                answer = data.get(f.read())
                f.close()
                if answer:
                    print(update.format(answer=answer, uuid=item.get('uuid')))
                    cur.execute(update.format(answer=answer, uuid=item.get('uuid')))
            except Exception:
                continue


if __name__ == '__main__':
    update()
