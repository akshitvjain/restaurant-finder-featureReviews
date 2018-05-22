# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector

class RestaurantreviewscraperSpider(scrapy.Spider):
	name = 'restaurantreviewscraper'
	allowed_domains = ['tripadvisor.in']
	start_urls = ['https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html']
	
	def parse(self, response):
		for restaurant in response.css('a.property_title'):
			res_url = ('https://www.tripadvisor.in%s' % restaurant.xpath('@href').extract_first())
			yield scrapy.Request(res_url, callback=self.parse_restaurant)

		next_page = ('https://www.tripadvisor.in%s'\
			% (response.css('a.nav.next.rndBtn.ui_button.primary.taLnk')).xpath('@href').extract_first())
		print('NEXT PAGE: ' + next_page)
		if next_page:
			yield scrapy.Request(next_page, callback=self.parse)
		
	def parse_restaurant(self, response):
		sel = Selector(response)
		print('Restaurant Name: %s' % sel.xpath('//h1/text()').extract()[1])
		addr_ = response.xpath('//div[@class="blEntry address  clickable colCnt2"]//span/text()').extract()
		addr = '%s | %s %s%s' % (addr_[0], addr_[1], addr_[2], addr_[3])
		print('Address: %s' % addr)
