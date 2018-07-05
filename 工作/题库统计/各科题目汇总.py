from 基础知识.数据库存储.Mysql import pymysql_util
import pymysql
from 基础知识.文档操作.excel import excel_util


def get_db():
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="juzi_yxy",
        password="nimo)OKM", db="topic_standard", port=42578,
        charset="utf8"
    )
    return db


# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
def book_sql(subject_code):
    sql = """SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id
        from t_res_chapter c
        LEFT JOIN t_res_units u on c.unit_id = u.unit_id
        LEFT JOIN t_res_book b on c.book_id = b.book_id
        LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id
        WHERE b.subject_code = '%s' 
        and b.book_name != '橘子学院营销培训'  group by c.chapter_id,gb.book_id"""
    return sql % subject_code

# 查询已入校的课本
# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
# def book_sql(subject_code):
#     sql = """SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id
#         from t_res_chapter c
#         LEFT JOIN t_res_units u on c.unit_id = u.unit_id
#         LEFT JOIN t_res_book b on c.book_id = b.book_id
#         LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id
#         WHERE b.subject_code = '%s'
#         and b.book_id in (SELECT f_material_id from t_teacher_material_map GROUP BY f_material_id)
#         and b.book_name != '橘子学院营销培训' group by c.chapter_id,gb.book_id"""
#     return sql % subject_code


# 查询运营反馈的版本
# ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
# def book_sql(subject_code):
#     sql = """SELECT b.subject_name,gb.grade,b.book_name,u.unit_name,c.chapter_name,b.edition_id,c.chapter_id
#         from t_res_chapter c
#         LEFT JOIN t_res_units u on c.unit_id = u.unit_id
#         LEFT JOIN t_res_book b on c.book_id = b.book_id
#         LEFT JOIN t_res_graduate_book gb on c.book_id = gb.book_id
#         WHERE b.subject_code = '%s' and b.book_id in ('030003001007038', '030003002007038', '030004001007038', '030004002007038', '030005001007038', '030005002007038', '010002001899844', '010002001988695', '010002002125100', '010002002505814', '010003001125100', '010003001857535', '010003002125100', '010003002203361', '010004001125100', '010004001629039', '010004002125100', '010004002897377', '010005001125100', '010005001340777', '010005002125100', '010005002759681', '010006001125100', '010006002125100', '240008001728351', '030003001968513', '030003002891332', '030004001885525', '030004002276316', '030005001821038', '030005002875972', '030006001413516', '030006002410659', '100008001200043', '100008002036100', '100008002240901', '240008001728657', '030007001020100', '030007002020100', '030008001020100', '030008002020100', '030009001020100', '030009002484622', '030003001016100', '030003001017100', '030003002016100', '030003002017100', '030004001016100', '030004001017100', '030004002016100', '030004002017100', '030005001016100', '030005001017100', '030005002016100', '030005002017100', '030006001016100', '030006001017100', '030006002016100', '030006002017100', '030003001007038', '030003001067100', '030003001087100', '030003001667371', '030003002007038', '030003002067100', '030003002087100', '030003002555655', '030004001007038', '030004001067100', '030004001087100', '030004001225132', '030004002007038', '030004002067100', '030004002087100', '030004002397286', '030005001007038', '030005001067100', '030005001087100', '030005002007038', '030005002067100', '030005002087100', '030006001007038', '030006001067100', '030006001087100', '030006002007038', '030006002067100', '030006002087100', '020001001004034', '020001002004034', '020002001004034', '020002002004034', '020003001004034', '020003002004034', '020004001004034', '020004002004034', '020005001004034', '020005002004034', '020006001004034', '020006002004034', '010002001012045', '010002002012045', '240008001728758', '240008001728759', '240008001728860', '050008001074100', '050008002074100', '050009001074100', '050009002074100', '010008002001001', '010007001096100', '010007002096100', '010008001096100', '010008002096100', '010009001096100', '010009002096100', '020007001139100', '020007002139100', '020008001139100', '020008002139100', '020009001139100', '020009002139100', '030007001102100', '030007002102100', '030008001102100', '030008002102100', '030009001220187', '030009002102100', '060008001948786', '060008002409041', '060009001055100', '060009001149022', '060009001544688', '060009002055100', '080007001082100', '080007002082100', '100007001106100', '100007002106100', '100008001106100', '100008002106100', '120007001602366', '120007002154100', '120008001393821', '120008002154100', '120009001796703', '120009002154100', '130007001155100', '130007002155100', '130008001703774', '130008002155100', '130009001155100', '130009002155100', '150007001068100', '150007002068100', '150008001068100', '150008002068100', '150009001068100', '150009002068100')
#         and b.book_name != '橘子学院营销培训' group by c.chapter_id,gb.book_id"""
#     return sql % subject_code


# 查询题目数量
# def sql_count_new(subject_key):
#     sql = """SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q
#           on qc.question_uuid = q.uuid where type in ('2','11')
#           GROUP BY qc.chapter_id"""
#     return sql % (subject_key, subject_key)


# # 查询新增题目数量
def sql_count_new(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc " \
          "where create_time >= '2018-05-22'  GROUP BY qc.chapter_id"
    return sql % subject_key


# 查询二月份之前录入题目数量
def sql_count_old(subject_key):
    sql = "SELECT qc.chapter_id,count(qc.question_uuid) from t_res_%s_question_chapter qc LEFT JOIN t_res_%s_question q "
    sql += "on qc.question_uuid = q.uuid where type in ('2','11') "
    sql += "and q.create_time < '2018-02-01 00:00:00' GROUP BY qc.chapter_id"
    return sql % (subject_key, subject_key)


def main(subject_key, subject_code):
    result_new = pymysql_util.find_all(db, sql_count_new(subject_key))  # '章节id','数量'
    result_old = pymysql_util.find_all(db, sql_count_old(subject_key))

    editor_sql = "SELECT edition_id,CONCAT(press_name,edition_name) from t_res_editor"
    editors = pymysql_util.find_all(db, editor_sql)
    sum = 0
    result_book = pymysql_util.find_all(db, book_sql(subject_code))
    # ('语文', '9', '语文北师版九上', '第二单元', '口技', 'edition_id', 'chapter_id')
    result_data = [["学科", "年级", "教材", "课本", "单元", "章节", "数量"]]
    for book in result_book:
        li = [book[0], book[1], 0, book[2], book[3], book[4], 0]
        for editor in editors:  # 教材
            if editor[0] == book[5]:
                li[2] = editor[1]
        for result in result_new:  # 二月新增数量
            if book[6] == result[0]:
                li[6] = result[1]
                sum += result[1]
        result_data.append(li)
    if sum > 0:
        excel_util.create_excel(result_data, "F:/导出/22号之后录入题目统计/%s题目数量统计.xlsx" % book[0][0])
    return sum


if __name__ == '__main__':
    db = get_db()
    sub_key = ["yw", "sx", "yy", "dl", "hx", "ls", "wl", "zz", "sw", 'kx', "sp", "dd", "ty", "ms", "mu", "ps"]
    sub_name = ["010", "020", "030", "080", "060", "100", "050", "090", "070", "040", "160", "240", "110", "120", "130",
                "190"]
    data = 0
    for i in range(len(sub_key)):
        d = main(sub_key[i], sub_name[i])
        data += d
        print(sub_key[i], d)
    print(data)
