# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider
from scrapy.http import FormRequest
from student_info.items import PersonInfo
from student_info.spiders import load_lastnames


def gen_search_formdata(lastname):
    return {'search_last': lastname,
                'lastwc': 'b',
                'search_first': '',
                'firstwc': 'b',
                'BUTTON': 'Search by NAME',
                'referer': ''}


class SyracuseSpider(Spider):
    name = 'syracuse'
    allowed_domains = ['syracuse.org']
    start_urls = ['http://directory.syr.edu/directory/dir.cfm']
    lastnames = load_lastnames()

    def start_requests(self):
        url = self.start_urls[0]
        for lastname in self.lastnames:
            yield scrapy.http.FormRequest(url,
                                          formdata=gen_search_formdata(lastname),
                                          callback=self.parse_info)

    def parse_info(self, response):
        student_rows = response.xpath("//tr[contains(., 'Junior') or \
                                            contains(., 'Senior') or \
                                            contains(., 'Sophomore') or \
                                            contains(., 'Freshman') or \
                                            contains(., 'Graduate')]")
        
        for row in student_rows:
            i = PersonInfo()
            i['name'], i['major'], i['classification'] = [value.strip() for value in row.css('td::text').extract()[:3]]
            
            if len(i['name'].split()) > 2: continue
            i['email'] = row.css('a::attr(href)').extract_first().split(':')[-1]
            yield i

        
        try:
            next_page_request = FormRequest.from_response(response,
                                                          formname="form",
                                                          clickdata={'value': 'Next'},
                                                          callback=self.parse_info)
        except ValueError as e:
            return
        
        yield next_page_request
