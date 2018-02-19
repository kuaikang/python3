import calendar,time
cal = calendar.month(2018,2)
print("以下输出2018年2月份的日历:")
print(cal)
week = calendar.weekday(2018,2,19) # 获取某一天是周几
week_dict={0:"一",1:"二",2:"三",3:"四",4:"五",5:"六",6:"日"}
print("2018年2月19日是周%s"%week_dict.get(week))

y = time.localtime(time.time())[0]
print(y,"年是否是闰年:",calendar.isleap(y))
print("2000年-2018年之间闰年的个数:",calendar.leapdays(2000,2018))