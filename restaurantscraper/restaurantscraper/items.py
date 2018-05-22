# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantscraperItem(scrapy.Item):
    # the fields for the item are defined here like:

	restaurant_name = scrapy.Field()
	restaurant_addr = scrapy.Field()
