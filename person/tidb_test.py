import subprocess
import json
import pymysql
import sys


def get_db():
    try:
        db = pymysql.connect(
            host='192.168.125.123', port=5919, user='root', password='root', db='exueyun_test', charset='utf8'
        )
        return db
    except Exception as e:
        print(e)


db = get_db()
cur = db.cursor()
db.autocommit(True)


def parse(data):
    result = []
    for region in data.get('record_regions'):
        if region.get('region_id'):
            result.append([data.get('name'), data.get('name'), region.get('region_id'),
                           region.get('leader').get('store_id')])
    for item in data.get('indices'):
        for r in item.get('regions'):
            if r.get('region_id'):
                result.append(
                    [data.get('name'), item.get('name'), r.get('region_id'),
                     r.get('leader').get('store_id')])
    return result


def get_tables():
    cur.execute("SELECT table_name FROM information_schema.`TABLES` a WHERE a.TABLE_SCHEMA = 'exueyun_test';")
    return cur.fetchall()


def main(argv):
    if argv == '*':
        tables = get_tables()
        for table in tables:
            js = req(table[0])
            if js:
                result = parse(js)
                for d in result:
                    print("table_name:{}index:{}RegionId:{}      StoreId:{}".format(d[0].ljust(40), d[1].ljust(40), d[2], d[3]))

    if not argv.isdigit():
        response = req(argv)
        if response:
            data = parse(response)
            for d in data:
                print("table_name:{}index:{}RegionId:{}StoreId:{}".format(d[0], d[1], d[2], d[3]))

    if argv.isdigit():
        data_list = []
        tables = get_tables()
        for table in tables:
            js = req(table[0])
            if js:
                result = parse(js)
                for d in result:
                    data_list.append(d)
        for item in data_list:
            if item[2] == int(argv):
                print("table_name:{}index:{}RegionId:{}StoreId:{}".format(item[0], item[1], item[2], item[3]))


def req(table):
    httpAPI = "http://192.168.125.123:10080/tables/{}/{}/regions".format("exueyun_test", table)
    webContent = subprocess.check_output(["curl", "-sl", httpAPI])
    try:
        region_info = json.loads(webContent)
        return region_info
    except Exception:
        return None


if __name__ == '__main__':
    arg = sys.argv[1]
    main(arg)
    db.close()
    cur.close()