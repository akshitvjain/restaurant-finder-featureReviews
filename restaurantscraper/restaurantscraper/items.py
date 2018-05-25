# -*- coding: utf-8 -*-

# Define here the models for your scraped items

import scrapy

class RestaurantscraperItem(scrapy.Item):
    
	# the fields for the item are defined here like:
	rest_name = scrapy.Field()
	rest_addr = scrapy.Field()
	rest_rank = scrapy.Field()
	rest_rating = scrapy.Field()
	rest_price = scrapy.Field()
	rest_total_reviews = scrapy.Field()
	rest_reviews = scrapy.Field()
