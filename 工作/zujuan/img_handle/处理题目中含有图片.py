from common.mysql_util import mysql
import requests


def select_all(sql):
    with mysql(db="sit_exue_resource") as cur:
        cur.execute(sql)
        return cur.fetchall()


def download(url):
    resp = requests.get(url=url)
    print(resp.headers)


def main():
    data = select_all("select * from t")


if __name__ == '__main__':
    pass
