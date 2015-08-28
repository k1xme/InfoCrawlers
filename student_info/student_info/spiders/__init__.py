# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import xlrd

def load_lastnames():
    try:
        workbook = xlrd.open_workbook('/Users/Kexi/Dev/crawlers/lastnames.xls')
    except Exception as e:
        raise "Lastname file does not exist\n"

    sheet = workbook.sheet_by_index(1)
    cells = sheet.col(1)[1:]

    return [cell.value for cell in cells]

def gen_start_urls(url_tmp):
    lastnames = load_lastnames()
    urls = [url_tmp % lastname for lastname in lastnames]
    return urls
