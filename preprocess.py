# -*- coding: utf-8 -*-
from pymongo import MongoClient
import pandas as pd

class PreprocessRestaurantItem(object)
	
	db_name = 'restaurantinfo'	

	def __init__(self): 
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = client[db_name]
	
	def mongodb_to_pandas(self):
		pass
