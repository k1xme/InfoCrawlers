import xlwt
import sys
from pymongo import MongoClient


client = MongoClient()


def dump_to_excel(cname):
    collection = client.student_info[cname]
    wb = xlwt.Workbook()
    ws = wb.add_sheet("info")
    row = 1
    ws.write(0, 0, "Full Name")
    ws.write(0, 1, "Major")
    ws.write(0, 2, "Year")
    ws.write(0, 3, "Email")

    for info in collection.find():
        ws.write(row, 0, info['name'])
        ws.write(row, 1, info['major'])
        ws.write(row, 2, info['classification'])
        ws.write(row, 3, info['email'])
        row += 1

    wb.save("%s.xls" % cname)

if __name__ == '__main__':
    cname = sys.argv[1]
    dump_to_excel(cname)
