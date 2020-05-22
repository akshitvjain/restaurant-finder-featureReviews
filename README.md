## Restaurant Finder

### Description
* Built a web crawler using Scrapy to collect restaurant information and reviews from TripAdvisor.
* Performed web scraping, cleaning and preprocessing of restaurant data before storing in MongoDB.
* Removed stop words, punctuations, special characters, numbers, and white-spaces from user reviews, and built a corpus applying tokenization and stemming.
* Identified key restaurant features from user reviews using Apriori algorithm and NLP.
* Generated summarized reviews based on frequent restaurant features.
* Created intelligent dashboards using Tableau to discover top restaurants by positive and negative reviews, cuisine, feature/meal, price, and location.
* Built a Flask application for users to search for restaurants based on their preference. The application also displays a feature based reviews for the searched restaurant and provides restaurant statistics by city along with other key information.

### Code
1. [Restaurant Scraper](https://github.com/akshitvjain/restaurant-reviews/tree/master/restaurantscraper)
2. [Data Cleaning and Processing for Analysis](https://github.com/akshitvjain/restaurant-reviews/blob/master/analysis-rest.py)
3. [Feature Review and Sentiment Analysis](https://github.com/akshitvjain/restaurant-reviews/blob/master/preprocess.py)
4. [Web Application](https://github.com/akshitvjain/restaurant-reviews/tree/master/restaurantapp)

### Data Visualization
1. [UK Map - Filter by City/Price/Cuisine/Meal/Feature](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/FilterRestDashboard)
2. [Restaurant Statistics - Filter by City](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/RestaurantStatistics)
3. [Categorical/Positive/Negative Review Count - Filter by City](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/ReviewsDashboard)

### Screenshots (Restaurant App)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%203.40.00%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%203.40.39%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.04.56%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.25.59%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.05.27%20PM.png)

### Programming Language
Python

### Technologies
Scrapy, MongoDB, Flask

### Tools/IDE
Tableau, MacOS Terminal(Vim)
