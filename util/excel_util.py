import csv
import sys

import xlwt

reload(sys)
sys.setdefaultencoding('utf-8')


def csv_to_xls(filename):
    my_excel = xlwt.Workbook(encoding='utf-8')
    my_sheet = my_excel.add_sheet("sheet1")
    csv_file = open(filename, "rb")
    reader = csv.reader(csv_file)
    l = 0
    for line in reader:
        r = 0
        for i in line:
            my_sheet.write(l, r, i)
            r = r + 1
        l = l + 1
    excel_filename = str(filename.split(".")[0]) + ".xls".encode('utf-8')
    my_excel.save(excel_filename.decode('utf-8'))
    return excel_filename
