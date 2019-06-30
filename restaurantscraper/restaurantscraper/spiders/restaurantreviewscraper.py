# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.selector import Selector
from selenium import webdriver
from restaurantscraper.items import RestaurantscraperItem

MAX_RESTAURANTS = 15	# collect information from each
MAX_REVIEWS = 10		# collect reviews from each restaurants

class RestaurantreviewscraperSpider(scrapy.Spider):
	name = 'restaurantreviewscraper'
	allowed_domains = ['tripadvisor.com']
	start_urls = [
		#"https://www.tripadvisor.in/Restaurants-g186525-Edinburgh_Scotland.html"	
		#"https://www.tripadvisor.com/Restaurants-g186338-London_England.html"
		#"https://www.tripadvisor.in/Restaurants-g186220-Bristol_England.html"
		#https://www.tripadvisor.in/Restaurants-g186411-Leeds_West_Yorkshire_England.html"
		#"https://www.tripadvisor.in/Restaurants-g187069-Manchester_Greater_Manchester_England.html"
		"https://www.tripadvisor.in/Restaurants-g186402-Birmingham_West_Midlands_England.html"
		#"https://www.tripadvisor.in/Restaurants-g186337-Liverpool_Merseyside_England.html"

	]	
	
	def __init__(self):
		self.restaurants_scraped = 0
		
	def parse(self, response):
		# yield restaurant information
		for restaurant in response.css('a.property_title'):
			self.restaurants_scraped += 1
			if (self.restaurants_scraped > MAX_RESTAURANTS):
				return
			res_url = ('https://www.tripadvisor.com%s' % \
				restaurant.xpath('@href').extract_first())
			yield scrapy.Request(res_url, callback=self.parse_restaurant)

		# move to the next page of restaurants
		next_page = ('https://www.tripadvisor.com%s'\
			% (response.css('a.nav.next.rndBtn.ui_button.primary.taLnk')) \
										.xpath('@href').extract_first())
		print('NEXT PAGE: ' + next_page)
		if next_page:
			yield scrapy.Request(next_page, callback=self.parse)
		
	def parse_restaurant(self, response):
		hasReviews = True
		sel = Selector(response)

		# start the webdriver to crawl reviews
		driver = webdriver.Chrome()

		# initialize Item class to access the fields
		rest_item = RestaurantscraperItem()

		# extract restaurant name
		rest_item['rest_name'] = sel.xpath('//h1/text()').extract()[1]

		# extract restaurant addr 
		street = response.xpath('//*[@id="taplc_resp_rr_top_info_rr_resp_0"]/div/div[4]/div[1]/div/div/div[1]/span[2]/span[1]/text()').extract_first()
		city = response.xpath('//*[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[4]/a/span/text()').extract_first()
		country = response.xpath('//*[@id="taplc_trip_planner_breadcrumbs_0"]/ul/li[3]/a/span/text()').extract_first()
		rest_item['rest_street'] = street
		rest_item['rest_city'] = city
		rest_item['rest_country'] = country

		# extract cuisine info
		rest_item['rest_cuisines'] = \
			response.xpath('//*[@id="taplc_restaurants_detail_info_content_0"]/div[2]/div/div[2]/div[2]/text()').extract_first()

		# extract ratings
		if (response.css('span.overallRating')):
			rest_item['rest_rating'] = float(response.css('span.overallRating::text').extract_first())
		else:
			rest_item['rest_rating'] = 0

		# extract price
		rest_item['rest_price'] = \
			response.xpath('//*[@id="taplc_resp_rr_top_info_rr_resp_0"]/div/div[3]/div[3]/div/a[1]/text()').extract_first()

		# extract restaurant features	

		"""
		row_four_features = \
		(response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[4]/div[1]/text()').extract_first().replace("\n", ""))
		row_five_features = \
		(response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[4]/div[1]/div[5]/div[1]/text()').extract_first().replace("\n", ""))
		
		if ( == "Restaurant features"):
			rest_item['rest_features'] = \
			response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[4]/div[2]/text()').extract_first()
		elif (row_five_features == "Restaurant features"):
			rest_item['rest_features'] = \
			response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[5]/div[2]/text()').extract_first()
		else:
			rest_item['rest_features'] = None 

		# extract restaurant meals
		
		row_three_meals = \
		(response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[3]/div[1]/text()').extract_first().replace("\n", ""))
		row_four_meals = \
		(response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[4]/div[1]/text()').extract_first().replace("\n", ""))

		if (row_three_meals == "Meals"):
			rest_item['rest_meals'] = \
			response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[3]/div[2]/text()').extract_first()
		elif (row_four_meals == "Meals"):
			rest_item['rest_meals'] = \
			response.xpath('//*[@id="RESTAURANT_DETAILS"]/div[2]/div[1]/div[4]/div[2]/text()').extract_first()
		else:
			rest_item['rest_meals'] = None
		"""

		# extract positive and negative reviews count
		excellent_count = int(response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]/span[2]/text()').extract_first())
		good_count = int(response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/span[2]/text()').extract_first())	
		rest_item['review_excellent_count'] = excellent_count 
		rest_item['review_good_count'] = good_count

		avg_count = int(response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/span[2]/text()').extract_first())
		poor_count = int(response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[4]/span[2]/text()').extract_first())
		terrible_count = int(response.xpath('//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[5]/span[2]/text()').extract_first())
		rest_item['review_avg_count'] = avg_count 
		rest_item['review_poor_count'] = poor_count
		rest_item['review_terrible_count'] = terrible_count

		# extract total number of reviews 
		if (response.xpath('//*[@id="REVIEWS"]/div[1]/div/div[1]/span/text()')):
			rest_item['rest_total_reviews'] = \
			int(response.xpath('//*[@id="REVIEWS"]/div[1]/div/div[1]/span/text()') \
								.extract_first().strip('()').replace(",", ""))
		else:
			hasReviews = False
			rest_item['rest_total_reviews'] = 0

		# extract reviews 
		if hasReviews:
			reviews = []
			url = response.url
			try:
				driver.get(url)
			except:
				pass
			time.sleep(4)
			while len(reviews) < MAX_REVIEWS:
				reviews += self.parse_reviews(driver)
				print('Fetched a total of {} reviews by now.'.format(len(reviews)))
				next_button = driver.find_element_by_class_name('next')
				if 'disabled' in next_button.get_attribute('class'):
					break
				next_button.click()
				time.sleep(5)
			rest_item['rest_reviews'] = reviews
			driver.close()
		yield rest_item

	def parse_reviews(self,driver):
		reviews = []
		try:
			driver.find_element_by_class_name('ulBlueLinks').click()
		except:
			pass
		time.sleep(5)
		review_containers = driver.find_elements_by_class_name('reviewSelector')
		for review in review_containers:
			review_text = review.find_element_by_class_name('partial_entry').text.replace('\n', '')
			reviews.append(review_text)
		return reviews
