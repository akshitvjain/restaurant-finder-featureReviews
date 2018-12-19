from pymongo import MongoClient
from flask import render_template
from app import app

client = MongoClient("mongodb://127.0.0.1:27017/restaurantinfo")
db = client['restaurantinfo']

@app.route('/')
@app.route('/home')
def home():
	restaurant = db.restaurantreviews.find({}, {"rest_name":1, "_id":0})
	for doc in restaurant:
		print(doc)
		return render_template('home.html', user=doc)
@app.route('/search')
def search():
	return render_template('search.html')

