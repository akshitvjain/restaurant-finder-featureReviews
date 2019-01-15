from pymongo import MongoClient
from flask import flash, render_template, request, redirect
from app import app
import csv
import pandas as pd

client = MongoClient("mongodb://127.0.0.1:27017/restaurantinfo")
db = client['restaurantinfo']

restaurant_review_collection = []
with open('app/feature_review_summary.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	for row in reader:
		restaurant_review_collection.append(row)
csvFile.close()

col_names = restaurant_review_collection.pop(0)
rest_df = pd.DataFrame(restaurant_review_collection, columns=col_names, index=None)

@app.route('/')
@app.route('/home')
def home():
	return render_template('home.html')

@app.route('/search')
def search():
	return render_template('search.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
	if request.method == 'POST':
		result = request.form
		rest = result['Restaurant Name']
		restaurant = db.restaurantreviews.find({}, {"rest_name":1, "_id":0})
		for r in restaurant:
			if (r['rest_name'].lower() == rest.lower()):
				# extract feature-review data from csv converted pandas df
				feature_review = dict() # store feature-review 
				if (rest_df['restaurant name'].isin([rest.lower()]).any()):
					# get features 
					features = rest_df.loc[rest_df['restaurant name'] == rest.lower(), 'feature'].tolist()
					# get reviews
					reviews = rest_df.loc[rest_df['restaurant name'] == rest.lower(), 'review'].tolist()
					# create a dictionary for feature-review
					for i in range(len(features)):
						if features[i] in feature_review:
							feature_review[features[i]].append(reviews[i])
						else:
							feature_review[features[i]] = [reviews[i]]
					length = [len(x) for x in feature_review.values()]
					print(length)
				# parse restaurant and feature-review data to render template
				if (db.restaurantreviews.find( {'rest_name' : r['rest_name'] } )):
					restaurant_info = db.restaurantreviews.find( {'rest_name' : r['rest_name'] }) 
					return render_template("result.html", rest_info=restaurant_info[0], feature_review=feature_review, length=length)			
		return render_template("noresult.html")

@app.route('/stats')
def stats():
	return render_template('stats.html')
