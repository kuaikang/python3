openpyxl（可读写excel表）专门处理Excel2007及以上版本产生的xlsx文件，xls和xlsx之间转换容易
注意：如果文字编码是“gb2312” 读取后就会显示乱码，请先转成Unicode
openpyxl定义多种数据格式
最重要的三种：
    NULL空值：对应于python中的None，表示这个cell里面没有数据。
    numberic： 数字型，统一按照浮点数来进行处理。对应于python中的float。
    string： 字符串型，对应于python中的unicode。
Excel文件三个对象:
    workbook： 工作簿，一个excel文件包含多个sheet。
    sheet：工作表，一个workbook有多个，表名识别，如“sheet1”,“sheet2”等。
    cell： 单元格，存储数据对象
WorkSheet属性:
    rows: 返回所有有效数据行,有数据时类型为generator,无数据时为tuple
    columns:返回所有有效数据列,类型同rows
    max_column:有效数据最大列
    max_row:有效数据最大行
    min_column:有效数据最小列,起始为1
    min_row:有效数据最大行,起始为1
    values:返回所有单元格的值的列表,类型为tuple
    title:WorkSheet的名称