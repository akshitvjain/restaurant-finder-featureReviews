# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from restaurantscraper.items import RestaurantscraperItem

class RestaurantreviewscraperSpider(scrapy.Spider):
	name = 'restaurantreviewscraper'
	allowed_domains = ['tripadvisor.in']
	start_urls = ['https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html']
	
	def parse(self, response):
		# yield restaurant information
		for restaurant in response.css('a.property_title'):
			res_url = ('https://www.tripadvisor.in%s' % \
				restaurant.xpath('@href').extract_first())
			yield scrapy.Request(res_url, callback=self.parse_restaurant)

		# move to the next page of restaurants
		next_page = ('https://www.tripadvisor.in%s'\
			% (response.css('a.nav.next.rndBtn.ui_button.primary.taLnk')) \
										.xpath('@href').extract_first())
		print('NEXT PAGE: ' + next_page)
		if next_page:
			yield scrapy.Request(next_page, callback=self.parse)
		
	def parse_restaurant(self, response):
		hasReviews = True
		sel = Selector(response)
		# initialize Item class to access the fields
		rest_item = RestaurantscraperItem()
		# extract restaurant name
		rest_item['rest_name'] = sel.xpath('//h1/text()').extract()[1]
		# extract restaurant addr 
		rest_item['rest_addr'] = response.xpath('//div[@class="blEntry address  \
									clickable colCnt2"]//span/text()').extract() 
		# extract restaurant rank
		if (response.css('div.prw_rup.prw_restaurants_header_eatery_pop_index')):
			rest_item['rest_rank'] = sel.xpath('//b/span/text()').extract()[0]
		else:
			rest_item['rest_rank'] = 'N/A'
		# extract number of reviews 
		if (response.css('a.seeAllReviews')):
			rest_item['rest_total_reviews'] = response.css('a.seeAllReviews::text') \
												.extract_first().strip(' reviews\n')
		else:
			hasReviews = False
			rest_item['rest_total_reviews'] = 'N/A'
		if hasReviews:
			pass	
		yield rest_item
