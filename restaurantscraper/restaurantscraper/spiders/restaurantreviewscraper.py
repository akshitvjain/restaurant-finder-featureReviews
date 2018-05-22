# -*- coding: utf-8 -*-
import scrapy


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
		print(response.xpath('//div[@class="blEntry phone"]//span/text()').extract_first())
        
