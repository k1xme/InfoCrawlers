InfoCrawlers
===

This is a test project that utilizes Scrapy to scrape person info from the public directory site of universities.
---

####Dependencies:
- PyMongo
- Scrapy
- xlwt
- xlrd


####Before Running:
Remember to put a `lastname.xls` file with the lastnames in the second column in the root directory of this project.


All 3 spiders are of `scrapy.spiders.Spider`.

- `miami_univ` is featured with the capabilities of handling multiple sessions withn one spider instance.
- `syracuse` is capable of generating FormRequest from responses.
- `isu_students` follows the links extracted from target entries(e.g. student entries) and scrapes detail infomation from the detail page.

