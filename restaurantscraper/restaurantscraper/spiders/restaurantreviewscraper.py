# -*- coding: utf-8 -*-
import scrapy


class RestaurantreviewscraperSpider(scrapy.Spider):
	name = 'restaurantreviewscraper'
	allowed_domains = ['tripadvisor.in']
	start_urls = ['https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html',
				'https://www.tripadvisor.in/Restaurants-g304551-New_Delhi_National_Capital_Territory_of_Delhi.html',
				]
	
	def parse(self, response):
		for restaurant in response.css('a.property_title'):
			res_url = ('https://www.tripadvisor.in%s' % restaurant.xpath('@href').extract_first())
			yield scrapy.Request(res_url, callback=self.parse_restaurant)
			return
	def parse_restaurant(self, response):
		print(response.xpath('//div[@class="blEntry phone"]//span/text()').extract_first())
        
