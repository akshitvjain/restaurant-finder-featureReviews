from pymongo import MongoClient
from flask import render_template
from app import app

#client = MongoClient("mongodb://127.0.0.1:27017/restaurantinfo")
#db = client['restaurantinfo']

@app.route('/')
@app.route('/index')
def index():
	user = {'username': 'Akshit Jain'}
	#restaurant = db.restaurantreviews.find({"rest_name" : "Amrutha Lounge"})
	return render_template('index.html', user=user)
