# -*- coding: utf-8 -*-
from pymongo import MongoClient
import re
import pandas as pd
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

class ProcessRestaurantItem(object):
	
	db_name = 'restaurantinfo'
	fields = ['rest_name', 'rest_rank', 'rest_addr', 'rest_rating', 'rest_price', 'rest_total_reviews', 'rest_reviews']
	df = None

	def __init__(self): 
		# Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]

	def load_mongodb_to_pandas(self):	
		restaurants = []
		for doc in self.db.restaurantreviews.find():
			restaurants.append([doc['rest_name'], doc['rest_rank'], doc['rest_addr'],
								doc['rest_rating'], doc['rest_price'],
								doc['rest_total_reviews'], doc['rest_reviews']])
		self.df = pd.DataFrame(restaurants, columns=self.fields)

	def decontracted(self, review):
		# specific
		review = re.sub(r"won't", "will not", review)
		review = re.sub(r"can\'t", "can not", review)
		# general
		review = re.sub(r"n\'t", " not", review)
		review = re.sub(r"\'re", " are", review)
		review = re.sub(r"\'s", " is", review)
		review = re.sub(r"\'d", " would", review)
		review = re.sub(r"\'ll", " will", review)
		review = re.sub(r"\'t", " not", review)
		review = re.sub(r"\'ve", " have", review)
		review = re.sub(r"\'m", " am", review)
		return review
		
	def add_rest_features(self, freq_features):
		manual_rest_features = ['value', 'location', 'food', 'service',
								'price', 'atmosphere', 'vibe', 'cuisine',
								'ambience', 'decor', 'quality']
		freq_features.extend(manual_rest_features)
		return freq_features

	def frequent_itemsets(self, rest_features):
		te = TransactionEncoder()
		te_ary = te.fit(rest_features).transform(rest_features)
		freq_df = pd.DataFrame(te_ary, columns=te.columns_)
		frequent_itemsets = apriori(freq_df, min_support=0.1, use_colnames=True)
		# collect all frequent features
		freq_features = []
		for itemset in frequent_itemsets['itemsets']:
			for item in itemset:
				freq_features.append(item)
		freq_features = self.add_rest_features(freq_features)
		return set(freq_features)
	
	def extract_opinion_words(self, freq_features, review_df):
		opinion_words = list()
		for review_sent in review_df['review_sent']:
			review_no_tag = [words[0] for words in review_sent]
			for feature in freq_features:
				if feature in review_no_tag:
					for words in review_sent:
						if (words[1] == 'JJ'):
							opinion_words.append(words[0].lower())
		return set(opinion_words)
	
	def process_reviews(self):
		# one restaurant at a time -> summarize reviews 
		for i, review_collection in enumerate(self.df['rest_reviews']):
			# collection of restraunt specific pos-tagged review sentences
			tagged_reviews_sent = []
			# collection of features in the reviews
			rest_features = []
			for j, rev in enumerate(review_collection):	
				review_sentences = rev.split('. ')
				for sentence in review_sentences:
					# contraction to decontraction
					sentence = self.decontracted(sentence)
					# remove punctuation
					sentence = re.sub(r'[^\w\s]','', sentence)
					# tokenize sentence
					token_sentence = nltk.word_tokenize(sentence)
					# part-of-speech tagging
					pos_tag_sentence = nltk.pos_tag(token_sentence)
					tagged_reviews_sent.append(pos_tag_sentence)
					# extract nouns as features from the review sentence
					# using chunking with regular expressions
					grammar = r'''
						NP: {<NNS><NN>}
							{<NN>}
					'''
					# regex for noun phrases: {<DT|PP\$>?<JJ>*<NN.*>+} 
					exp = nltk.RegexpParser(grammar)
					sent_tree = exp.parse(pos_tag_sentence)
					features = []
					for subtree in sent_tree.subtrees():
						if (subtree.label() == 'NP'):
							nps = ' '.join(word[0] for word in subtree.leaves())
							features.append(nps)
							# remove stopwords
							features = [feat.lower() for feat in features if i not in stop]
							# lemmatize feature words
							features = [lmtzr.lemmatize(feat) for feat in features]	
					if len(features) != 0:
						rest_features.append(features)
			# convert lists to numpy array
			tagged_reviews_sent = np.array(tagged_reviews_sent)
			# store pos tagged sentences in a dataframe for processing
			review_df = pd.DataFrame(tagged_reviews_sent, columns=['review_sent'])
			freq_features = self.frequent_itemsets(rest_features)
			opinion_words = self.extract_opinion_words(freq_features, review_df)
			print(opinion_words)
									
if __name__ == '__main__':
	process = ProcessRestaurantItem()
	process.load_mongodb_to_pandas()
	process.process_reviews()