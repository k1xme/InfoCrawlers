# -*- coding: utf-8 -*-
import scrapy
from student_info.items import PersonInfo
from student_info.spiders import gen_start_urls, load_lastnames


class StudentsSpider(scrapy.Spider):
    name = "isu"
    allowed_domains = ["info.iastate.edu"]
    url_tmp = "http://info.iastate.edu/individuals/advanced?last_name=%s&individual_type=students"
    # start_urls = gen_start_urls()
    lastnames = load_lastnames()
    start_urls = gen_start_urls(url_tmp)

    def parse(self, response):
        links = [response.urljoin(a.extract()) for a in response.css(".dir-Listing-item::attr('href')")]
        for link in links:
            lastname = link.split("/")[-1].split("-")[0]
            if lastname not in self.lastnames: continue

            yield scrapy.Request(link, self.parse_info)

        paginations = response.css(".wd-Pagination > li").xpath("//a[text()='Next']//@href")

        if not paginations: return

        next_page_url = response.urljoin(paginations[-1].extract())

        # Request next page
        yield scrapy.Request(next_page_url, self.parse)


    def parse_info(self, response):
        h1 = response.css(".wd-l-Content-inner > h1::text")
        # No Name here
        if not h1: return
        info_section = response.css(".dir-Person")

        person = PersonInfo()
        person["name"] = h1.extract()[0]
        email = info_section.xpath("div[contains(./span, 'Email:')]/ins//text()").extract()[0]

        if not email: return
        
        person["email"] = email.replace(u" (at) ", u"@").replace(u" (dot) ", u".")
        major_cls_section = info_section.xpath("div[contains(*/span, 'Major:')]").css(".dir-Person-item")
        
        if not major_cls_section: return

        person["major"] = major_cls_section[0].xpath("text()").extract()[0]
        person["classification"] = major_cls_section[1].xpath("text()").extract()[0]

        return person



