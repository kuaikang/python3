from openpyxl.workbook import Workbook


def create_excel(data, file):
    """生成excel"""
    wb = Workbook()
    ws = wb.active
    length = len(data)
    for line in range(length):
        cols = len(data[line])
        for j in range(cols):
            ws.cell(row=line + 1, column=j + 1, value=data[line][j])
    wb.save(file)
