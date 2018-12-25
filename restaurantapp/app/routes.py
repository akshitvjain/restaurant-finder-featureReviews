from pymongo import MongoClient
from flask import flash, render_template, request, redirect
from app import app

client = MongoClient("mongodb://127.0.0.1:27017/restaurantinfo")
db = client['restaurantinfo']

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
				if (db.restaurantreviews.find( {'rest_name' : r['rest_name'] } )):
					restaurant_info = db.restaurantreviews.find( {'rest_name' : r['rest_name'] } )
					return render_template("result.html", result=restaurant_info[0])			
		return render_template("noresult.html")
