# -*- coding: utf-8 -*-
from pymongo import MongoClient
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords
#stop = stopwords.words('english')

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
		for i, review_collection in enumerate(self.df['rest_reviews']):
			for j, rev in enumerate(review_collection):	
				review_sentences = rev.split('. ')
				for sentence in review_sentences:
					# convert to lowercase
					sentence = sentence.lower()
					# remove punctuation
					sentence = re.sub(r'[^\w\s]','', sentence)
					# tokenize sentence
					token_sentence = nltk.word_tokenize(sentence)
					# part-of-speech tagging
					pos_tag_sentence = nltk.pos_tag(token_sentence)
					print(pos_tag_sentence)
				return
						
if __name__ == '__main__':
	preprocess = PreprocessRestaurantItem()
	preprocess.load_mongodb_to_pandas()
	preprocess.preprocess_reviews()