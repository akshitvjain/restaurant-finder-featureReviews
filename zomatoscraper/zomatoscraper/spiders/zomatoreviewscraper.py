# -*- coding: utf-8 -*-
import scrapy


class ZomatoreviewscraperSpider(scrapy.Spider):
    name = 'zomatoreviewscraper'
    allowed_domains = ['www.zomato.com/mumbai/']
    start_urls = ['http://www.zomato.com/mumbai//']

    def parse(self, response):
        pass
