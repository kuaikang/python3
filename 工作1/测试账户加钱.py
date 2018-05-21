from common.mysql_util import mysql

if __name__ == '__main__':
    res = ['18410000000', '18410000001', '18410000002', '18410000003', '18410000004', '18410000005', '18410000006',
           '18410000007', '18210000008']
    with mysql(db="sit2_exue") as cur:
        for r in res:
            cur.execute(
                "SELECT * from sit2_exue.t_user_base WHERE s_phone = '{phone}' and s_is_delete = '0'".format(phone=r))
            data = cur.fetchone()
            if data:
                print(
                    "update sit2_exue_pay.t_pay_user_account set s_money = '100000' WHERE  f_user_id = '{user_id}';".format(
                        user_id=data.get('p_id')))
