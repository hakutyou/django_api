import csv
import datetime

import time
import xlrd

from api.service import app

EXCEL_DATE = 3


@app.task(bind=True)
# celery 测试
def add(_, x, y):
    print('enter call function ...')
    time.sleep(1)
    return x + y


def read_xls(filename, sheet_index=0):
    def read_cell(sheet_cell):
        value = sheet_cell.value
        if sheet_cell.ctype == EXCEL_DATE:
            value = xlrd.xldate_as_tuple(value, workbook.datemode)
            value = datetime.date(*value[:3])  # .strftime('%Y/%m/%d')
        return value

    workbook = xlrd.open_workbook(filename=filename)
    # print(workbook.sheet_names())
    sheet = workbook.sheet_by_index(sheet_index)
    nrows, ncols = sheet.nrows, sheet.ncols
    print(f'{nrows}x{ncols}')
    print(sheet.merged_cells)

    for y in range(nrows):
        for x in range(ncols):
            # 合并单元格
            cell_value = read_cell(sheet.cell(y, x))
            for merged in sheet.merged_cells:
                if merged[0] <= y < merged[1] and merged[2] <= x < merged[3]:
                    cell_value = read_cell(sheet.cell(merged[0], merged[2]))
            print(cell_value, end='\t')
        print('')


def read_csv(filename):
    sheet = csv.reader(open(filename, 'r'))
    for line in sheet:
        for atom in line:
            print(atom, end='\t')
        print('')
