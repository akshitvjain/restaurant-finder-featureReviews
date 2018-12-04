# -*- coding: utf-8 -*-
from pymongo import MongoClient
import numpy as np
import pandas as pd

class AnalyzeRestaurantItem(object):

	db_name = 'restaurantinfo'
	fields = ['rest_name', 'rest_rank', 'rest_addr', 'rest_rating', \
				'rest_price', 'rest_cuisines', 'rest_total_reviews']
	df = None

	def __init__(self):
		#Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]

	def load_mongodb_to_pandas(self):
		rest_info = []
		for doc in self.db.restaurantreviews.find():
			rest_info.append([doc['rest_name'], doc['rest_rank'], doc['rest_addr'], \
							doc['rest_rating'], doc['rest_price'], doc['rest_cuisines'], \
							doc['rest_total_reviews']])
		self.df = pd.DataFrame(rest_info, columns=self.fields)
		print(self.df)

if __name__ == '__main__':
	analyze = AnalyzeRestaurantItem()
	analyze.load_mongodb_to_pandas()
	
