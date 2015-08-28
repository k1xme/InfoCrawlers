# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from student_info.spiders import gen_start_urls, load_lastnames
from student_info.items import PersonInfo


class MiamiUnivSpider(CrawlSpider):
    url_tmp = 'https://community.miamioh.edu/phpapps/directory/?query_type=simple&query_operator=equals&query_filter_type=people&query_string=%%22%s%%22&run_query=Search'
    detail_url_tmp = r"\?query_type=simple&query_operator=equals&query_filter_type=people&query_string=%22\w+%22&show=\w+&start=\w+"
    name = 'miami_univ'
    lastnames = load_lastnames()
    start_urls = gen_start_urls(url_tmp)


    def start_requests(self):
        for i, url in enumerate(self.start_urls):
            yield scrapy.http.Request(url, meta={'cookiejar': i}, dont_filter=True)
    

    def parse_start_url(self, response):
        return self.parse_result_list(response)


    def parse_result_list(self, response):
        cookiejar = response.meta['cookiejar']
        target_lastname = self.lastnames[cookiejar]

        student_entries = response.css("ol").xpath("li[p[contains(text(), 'student')]]")
        for i, name in enumerate(student_entries.xpath("*/a/text()").extract()):
            name_parts = name.split()
            if len(name_parts) > 2 or name_parts[0].rstrip(",") != target_lastname: continue
            
            info_detail_url = student_entries[i].css("a::attr(href)").extract()[0]
            info_detail_url = response.urljoin(info_detail_url)
            
            yield scrapy.Request(info_detail_url, meta={'cookiejar': cookiejar},
                                                  callback=self.parse_info, dont_filter=True)

        next_page_url = response.css("#next_result_list a::attr(href)").extract()
        
        if next_page_url:
            next_page_url = response.urljoin(next_page_url[0])

            yield scrapy.Request(next_page_url, meta={'cookiejar': cookiejar},
                                                  callback=self.parse_result_list, dont_filter=True)



    def parse_info(self, response):
        i = PersonInfo()
        name = response.css(".entry_table h1::text").extract()[0]
        uid, cls, major = response\
                            .css(".attribute_group")\
                            .xpath("*/tr[td = 'UniqueID:' or td = 'Major:' or td = 'Class:']/*/p/text()")\
                            .extract()[:3]
        i['email'] = '%s@miamioh.edu' % uid
        i['name'] = name
        i['major'] = major
        i['classification'] = cls
        return i
