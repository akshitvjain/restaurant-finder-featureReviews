# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver
from restaurantscraper.items import RestaurantscraperItem

MAX_RESTAURANTS = 1000
MAX_REVIEWS = 200

class RestaurantreviewscraperSpider(scrapy.Spider):
	name = 'restaurantreviewscraper'
	allowed_domains = ['tripadvisor.in']
	start_urls = [
		'https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html'
	]	
	
	def __init__(self):
		self.restaurants_scraped = 0
		self.driver = webdriver.Chrome() 

	def parse(self, response):
		# yield restaurant information
		for restaurant in response.css('a.property_title'):
			self.restaurants_scraped += 1
			if (self.restaurants_scraped > MAX_RESTAURANTS):
				return
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
		rest_item['rest_addr'] = response.xpath \
			('//div[@class="blEntry address  clickable colCnt2"]//span/text()').extract() 
		# extract restaurant rank
		if (response.css('div.prw_rup.prw_restaurants_header_eatery_pop_index')):
			rest_item['rest_rank'] = sel.xpath('//b/span/text()').extract()[0]
		else:
			rest_item['rest_rank'] = None
		# extract ratings
		if (response.css('span.overallRating')):
			rest_item['rest_rating'] = float(response.css('span.overallRating::text').extract_first())
		else:
			rest_item['rest_rating'] = 0
		# extract price
		if (response.css('span.text')):
			rest_item['rest_price'] = response.css('span.text::text').extract_first() \
										.encode("utf-8").replace('\xe2\x82\xb9', 'r')
		else:
			rest_item['res_price'] = None
		# extract number of reviews 
		if (response.css('a.seeAllReviews')):
			rest_item['rest_total_reviews'] = \
			int(response.css('span.reviews_header_count.block_title::text') \
								.extract_first().strip('()').replace(",", ""))
		else:
			hasReviews = False
			rest_item['rest_total_reviews'] = 0
		# extract reviews 
		if hasReviews:
			reviews = []
			url = response.url
			try:
				self.driver.get(url)
			except:
				pass
			time.sleep(3)
			while len(reviews) < MAX_REVIEWS:
				reviews += self.parse_reviews()
				print('Fetched a total of {} reviews by now.'.format(len(reviews)))
				next_button = self.driver.find_element_by_class_name('next')
				if 'disabled' in next_button.get_attribute('class'):
					break
				next_button.click()
				time.sleep(4)
			rest_item['rest_reviews'] = reviews
			self.driver.close()
		yield rest_item

	def parse_reviews(self):
		reviews = []
		try:
			self.driver.find_element_by_class_name('ulBlueLinks').click()
		except:
			pass
		time.sleep(4)
		review_containers = self.driver.find_elements_by_class_name('reviewSelector')
		for review in review_containers:
			review_text = review.find_element_by_class_name('partial_entry').text.replace('\n', '')
			reviews.append(review_text)
		return reviews
