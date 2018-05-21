# -*- coding: utf-8 -*-
import scrapy


class RestaurantreviewscraperSpider(scrapy.Spider):
    name = 'restaurantreviewscraper'
    allowed_domains = ['yelp.com']
    start_urls = ['https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html']

    def parse(self, response):
        print(response.xpath('//div[@class="title"]/a/text()').extract_first())
