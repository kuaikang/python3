import pymysql
from common.excel_util import create_excel


def get_db(db):
    # 打开数据库连接
    db = pymysql.connect(
        host="192.168.121.159", user="dept_jz",
        password="nimo_PL<", db=db, port=42578,
        charset="utf8"
    )
    return db


select_school = """
        SELECT p_id,s_name,CONCAT(s_province_name,s_city_name,s_area_name) as area,s_period_name from t_school 
        WHERE s_province_name != '海北省' and s_name not like '%测试%' and s_name NOT regexp '^[0-9]+$' 
        and s_name not in ('辅导','发的发的','是','对方答复','品质');
        """
select_student_count = """SELECT count(DISTINCT f_student_id) as num from t_student_class_map m LEFT JOIN t_classes c on m.f_class_id = c.p_id
                    WHERE c.f_school_id = '{school_id}';
                    """
select_teacher_count = "SELECT count(1) as num from t_teacher_school_map WHERE f_school_id = '{school_id}';"
select_material_count = "SELECT * from t_teacher_material_map WHERE f_school_id = '{school_id}' GROUP BY f_material_id;"

uat = get_db(db="uat_exue")
cur_uat = uat.cursor(pymysql.cursors.DictCursor)
res = get_db(db="uat_exue_resource")
cur_res = res.cursor(pymysql.cursors.DictCursor)


def main():
    cur_uat.execute(select_school)
    schools = cur_uat.fetchall()
    result = [["学校名称", "地区", "主要学段", "学生数量", "老师数量", "语文版本", "数学版本", "英语版本"]]
    for s in schools:
        print(s)
        cur_uat.execute(select_student_count.format(school_id=s.get('p_id')))
        student_count = cur_uat.fetchone().get('num')
        cur_uat.execute(select_teacher_count.format(school_id=s.get('p_id')))
        teacher_count = cur_uat.fetchone().get('num')
        cur_res.execute(select_material_count.format(school_id=s.get('p_id')))
        materials = cur_res.fetchall()
        yw_material = ",".join(
            [item.get('s_material_name') for item in materials if '语文' in item.get('s_material_name')])
        sx_material = ",".join(
            [item.get('s_material_name') for item in materials if '数学' in item.get('s_material_name')])
        yy_material = ",".join(
            [item.get('s_material_name') for item in materials if '英语' in item.get('s_material_name')])
        result.append(
            [s.get('s_name'), s.get('area'), s.get('s_period_name'), student_count, teacher_count, yw_material,
             sx_material, yy_material])
    create_excel(result, "F:/入校情况.xlsx")


if __name__ == '__main__':
    main()
