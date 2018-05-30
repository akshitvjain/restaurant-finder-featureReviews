# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd
import spacy
nlp = spacy.load('en')
from spacy.lang.en.stop_words import STOP_WORDS

class PreprocessRestaurantItem(object):
	
	db_name = 'restaurantinfo'
	fields = ['rest_name', 'rest_rank', 'rest_addr', 'rest_rating', 'rest_price', 'rest_total_reviews', 'rest_reviews']
	df = None

	def __init__(self): 
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]
	
	def load_mongodb_to_pandas(self):	
		restaurants = []
		for doc in self.db.restaurantreviews.find():
			restaurants.append([doc['rest_name'], doc['rest_rank'], doc['rest_addr'],
								doc['rest_rating'], doc['rest_price'],
								doc['rest_total_reviews'], doc['rest_reviews']])
		self.df = pd.DataFrame(restaurants, columns=self.fields)

	def preprocess_reviews(self):	
		pass
		# TODO: cleaning and preprocessing text reviews
			
						

if __name__ == '__main__':
	preprocess = PreprocessRestaurantItem()
	preprocess.load_mongodb_to_pandas()
	preprocess.preprocess_reviews()