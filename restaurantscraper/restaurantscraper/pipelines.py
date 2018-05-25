# -*- coding: utf-8 -*-

# Define your item pipelines here

class RestaurantscraperPipeline(object):
    def process_item(self, item, spider):
		print(item)
        return item
