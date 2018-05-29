# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd

class PreprocessRestaurantItem(object):
	
	db_name = 'restaurantinfo'	

	def __init__(self): 
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]
	
	def load_mongodb_to_pandas(self):	
		restaurants = []
		for doc in self.db.restaurantreviews.find():
			restaurants.append([doc['rest_name'], doc['rest_rank']])
		df = pd.DataFrame(restaurants, columns=['rest_name', 'rest_rank'])
		print(restaurants)
		print(df)

if __name__ == '__main__':
	preprocess = PreprocessRestaurantItem()
	preprocess.load_mongodb_to_pandas()