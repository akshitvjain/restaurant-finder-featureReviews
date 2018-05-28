# -*- coding: utf-8 -*-

# Scrapy settings for restaurantscraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. 

BOT_NAME = 'restaurantscraper'

SPIDER_MODULES = ['restaurantscraper.spiders']
NEWSPIDER_MODULE = 'restaurantscraper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure item pipelines
ITEM_PIPELINES = {
    'restaurantscraper.pipelines.RestaurantscraperPipeline' : 300,
}
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'restaurantinfo'
