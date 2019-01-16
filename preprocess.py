# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from pymongo import MongoClient
import re
import pandas as pd
import numpy as np
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
lmtzr = WordNetLemmatizer()
from nltk.corpus import stopwords
stop = set(stopwords.words('english'))
from nltk.corpus import wordnet as wn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori

class ProcessRestaurantItem(object):
	
	db_name = 'restaurantinfo'
	fields = ['rest_name', 'rest_city', 'rest_reviews']
	df = None	

	def __init__(self): 
		# Setup Client for MongoDB
		self.client = MongoClient('mongodb://localhost:27017/restaurantinfo')
		self.db = self.client[self.db_name]

	def load_mongodb_to_pandas(self):	
		restaurants = []
		for doc in self.db.restaurantreviews.find():
			restaurants.append([doc['rest_name'], doc['rest_city'], doc['rest_reviews']])
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
	
	def opinion_orientation(self, opinion_words):
		# lists to save the opinion based on orientation
		# some initial opinion words
		pos_opinion = ['authentic', 'cheap', 'inexpensive', 'quick', 'warm', 'hot']
		neg_opinion = ['slow', 'expensive', 'disappointed', 'bland', 'overdone', 'overcooked']
		sid = SentimentIntensityAnalyzer()
		# grow the orientation lists based on user reviews
		for word in opinion_words:
			if sid.polarity_scores(word)['pos'] == 1.0:
				pos_opinion.append(word)
			elif sid.polarity_scores(word)['neg'] == 1.0:
				neg_opinion.append(word)
		return set(pos_opinion), set(neg_opinion)

	def sentence_orientation(self, pos_opinions, neg_opinions, review_df):
		sid = SentimentIntensityAnalyzer()
		processed_reviews = []
		for rev_sent in review_df['review_sent']:
			review_no_tag = [words[0] for words in rev_sent]
			str_r = ' '.join(review_no_tag)
			orientation = 0
			for word in review_no_tag:
				if word.lower() in pos_opinions or word.lower() in neg_opinions:
					orientation += self.word_orientation(word.lower(), pos_opinions,
														neg_opinions, review_no_tag)
			if orientation > 0:
				processed_reviews.append([str_r, 1])
			elif orientation < 0:
				processed_reviews.append([str_r, -1])
			else:
				pass
				# ori = sid.polarity_scores(str_r)['compound']	

		processed_reviews = np.array(processed_reviews)
		processed_reviews_df = pd.DataFrame(processed_reviews, columns=['reviews','sentiment'])
		return processed_reviews_df

	def word_orientation(self, word, pos_opinions, neg_opinions, review_no_tag):	
		if word in pos_opinions:
			if self.diff_negation(word, review_no_tag):
				return -1
			else:
				return 1
		elif word in neg_opinions:
			if self.diff_negation(word, review_no_tag):
				return 1
			else:
				return -1

	def diff_negation(self, word, review_no_tag):
		negation_words = ['no', 'not', 'yet', 'but', 'nevertheless', 'while'
						'however', 'instead', 'despite', 'although', 'though']
		review_no_tag = [w.lower() for w in review_no_tag]
		for nw in negation_words:
			if nw in review_no_tag:
				op_index = review_no_tag.index(word)
				nw_index = review_no_tag.index(nw)
				if abs(op_index - nw_index) <= 5:
					return True
		return False 
	
	def generate_summary(self, rest_name, city, freq_features, processed_reviews_df):
		feature_summary_reviews = []
		for feature in freq_features:
			for i, review in enumerate(processed_reviews_df['reviews']):
				if feature in review:
					feature_summary_reviews.append([rest_name.lower(), city, feature, review,
								processed_reviews_df['sentiment'][i]])
		feature_summary_df = pd.DataFrame(feature_summary_reviews, 
							columns=['restaurant name', 'city', 'feature', 'review', 'sentiment'])
		return feature_summary_df
			
	def process_reviews(self):
		df_collection = []
		# one restaurant at a time -> summarize reviews 
		for i, review_collection in enumerate(self.df['rest_reviews']):
			# get restaurant name
			rest_name = self.df['rest_name'][i]
			city = self.df['rest_city'][i]
			# collection of restraunt specific pos-tagged review sentences
			tagged_reviews_sent = []
			# collection of features in the reviews
			rest_features = []
			for j, rev in enumerate(review_collection):	
				review_sentences = rev.split('. ')
				for sentence in review_sentences:
					# contraction to decontraction
					sentence = self.decontracted(sentence)
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
							nps = ''.join(word[0] for word in subtree.leaves())
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
			# store the pos, neg opinion words
			pos_opinion, neg_opinion = self.opinion_orientation(opinion_words)
			processed_reviews_df = self.sentence_orientation(pos_opinion, neg_opinion, review_df)
			# generate feature based review summary
			feature_summary_df = self.generate_summary(rest_name, city, freq_features, processed_reviews_df)
			df_collection.append(feature_summary_df)
		feature_collection_summary = pd.concat(df_collection, ignore_index=True)
		feature_collection_summary.to_csv('restaurantapp/app/feature_review_summary.csv', index=False)
		
if __name__ == '__main__':
	process = ProcessRestaurantItem()
	process.load_mongodb_to_pandas()
	process.process_reviews()