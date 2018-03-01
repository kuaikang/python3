import xlrd,pymysql


def read_excel(url):
    # 打开文件
    workbook = xlrd.open_workbook(url)
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_name(workbook.sheet_names()[0])
    list = []
    for i in range(1,sheet.nrows):
        li = {}
        li["出版社"] = sheet.cell_value(i,0)
        li["教材"] = sheet.cell_value(i,1)
        li["版本号"] = sheet.cell_value(i, 2)
        li["科目"] = sheet.cell_value(i, 3)
        li["年级"] = int(sheet.cell_value(i, 4))
        list.append(li)
    return list


def insert_many(list):
    # 打开数据库连接
    db = pymysql.connect(host="192.168.0.168", port=3306, user="root", passwd='001233', db="kuaik", charset="utf8")
    # 使用cursor()方法获取游标对象
    cursor = db.cursor()
    # 使用预处理语句创建表
    try:
        # 执行sql
        sql = "INSERT INTO resource (`id`, `subject`, `publish`, `version`, `grade`, `material`) VALUES (%s,%s,%s,%s,%s,%s)"
        cursor.executemany(sql, list)
        # 提交到数据库执行
        db.commit()
    except Exception as e:
        # 如果发生错误
        print(e)
        db.rollback()
    # 关闭连接
    db.close()


def list_no_repeat(list):
    list_new = []
    for i in list:
        if i not in list_new:
            list_new.append(i)
    return list_new


if __name__ == '__main__':
    list1 = read_excel("E:\\QQ\\359405466\\FileRecv\\学乐云(1).xlsx");
    list2 = read_excel("E:\\QQ\\359405466\\FileRecv\\教材名称整理 (1-1).xlsx")
    # 去重
    list1_new = list_no_repeat(list1)

    num = 0
    list_dict = []
    for i in range(len(list1_new)):
        if list1_new[i] not in list2:
            list_dict.append(list1_new[i])
            num += 1
    print(num)
    # with open("1.txt",mode="w",encoding="utf-8") as f:
    #     f.write(str(list_dict).replace("'",'"'))

    list_sql = []
    id = 0
    for i in list_dict:
        l = (id,i["科目"],i["出版社"],i["版本号"],i["年级"],i["教材"])
        id += 1
        list_sql.append(l)