# -*- coding: utf-8 -*-

# Define here the models for your scraped items

import scrapy

class RestaurantscraperItem(scrapy.Item):
    
	# the fields for the item are defined here like:
	rest_name = scrapy.Field()
	rest_street = scrapy.Field()
	rest_city = scrapy.Field()
	rest_country = scrapy.Field()
	rest_rating = scrapy.Field()
	rest_price = scrapy.Field()
	rest_total_reviews = scrapy.Field()
	rest_cuisines = scrapy.Field()
	rest_reviews = scrapy.Field()
	review_excellent_count = scrapy.Field()
	review_good_count = scrapy.Field()
	review_avg_count = scrapy.Field()
	review_poor_count = scrapy.Field()
	review_terrible_count = scrapy.Field()
	rest_features = scrapy.Field()
	rest_meals = scrapy.Field() 
