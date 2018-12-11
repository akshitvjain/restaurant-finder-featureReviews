# -*- coding: utf-8 -*-
from pymongo import MongoClient
from geopy.geocoders import Nominatim
import numpy as np
import pandas as pd


class AnalyzeRestaurantItem(object):

	db_name = 'restaurantinfo'
	info_fields = ['rest_name', 'lat', 'lon', 'rest_street', 'rest_city', \
				'rest_country', 'rest_rating', 'review_excellent_count', \
				'review_good_count', 'review_avg_count', 'review_poor_count', \
				'review_terrible_count', 'positive_review_count', 'negative_review_count', \
				'rest_total_reviews']
	cuisine_fields = ['rest_name', 'cuisine', 'price']
	features_fields = ['rest_name', 'rest_features']
	meals_fields = ['rest_name', 'rest_meals']

	info_df = None
	cuisines_df = None
	features_df = None
	meals_df = None

	def __init__(self):

		#Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]


	def convert_addr_to_coord(self, addr):
		
		geolocator = Nominatim()
		location = geolocator.geocode(addr, timeout=3)
		if location:
			return location.latitude, location.longitude
		else:
			return 0,0

	def load_mongodb_to_pandas(self):

		rest_info = []
		rest_cuisine = []
		rest_features = []
		rest_meals = []
		for doc in self.db.restaurantreviews.find():
			street = doc['rest_street']
			city = doc['rest_city']
			country = doc['rest_country']
			lat, lon = self.convert_addr_to_coord(street + ", " + city + ", " + country)	
			if (lat != 0 and lon != 0):
				positive_review_count = int(doc['review_excellent_count']) + \
										int(doc['review_good_count'])
				negative_review_count = int(doc['review_avg_count']) + \
										int(doc['review_poor_count']) + \
										int(doc['review_terrible_count'])

				# load restaurant details, reviews
				rest_info.append([doc['rest_name'], float(lat), float(lon), doc['rest_street'], \
								doc['rest_city'], doc['rest_country'], doc['rest_rating'], \
								doc['review_excellent_count'], doc['review_good_count'], doc['review_avg_count'], \
								doc['review_poor_count'], doc['review_terrible_count'], \
								positive_review_count, negative_review_count, doc['rest_total_reviews']])

				# load restaurant cuisines, price data
				cuisines = doc['rest_cuisines'].split(',')
				for cuisine in cuisines:
					rest_cuisine.append([doc['rest_name'], cuisine.strip("\n"), doc['rest_price']])
				# load restaurant features
				features = doc['rest_features'].split(',')
				for feature in features:
					rest_features.append([doc['rest_name'], feature.strip("\n")])
				# load restaurant meals 
				meals = doc['rest_meals'].split(',')
				for meal in meals:
					rest_meals.append([doc['rest_name'], meal.strip("\n")])

		self.info_df = pd.DataFrame(rest_info, columns=self.info_fields)
		self.cuisines_df = pd.DataFrame(rest_cuisine, columns=self.cuisine_fields)
		self.features_df = pd.DataFrame(rest_features, columns=self.features_fields)
		self.meals_df = pd.DataFrame(rest_meals, columns=self.meals_fields)

		print(self.info_df)	
		print(self.cuisines_df)
		print(self.features_df)
		print(self.meals_df)

if __name__ == '__main__':
	analyze = AnalyzeRestaurantItem()
	analyze.load_mongodb_to_pandas()
	
