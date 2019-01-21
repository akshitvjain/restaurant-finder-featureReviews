## Restaurant Analysis & Finder - Web Scraping and Sentiment Analysis of Restaurant Info/Reviews on TripAdvisor (UK)

### Description
* Built a web crawler using Scrapy to collect restaurant information and reviews from TripAdvisor.
* Stored all the data in MongoDB after preprocessing/cleaning the reviews and other restaurant related information.
* Conducted data pre-processing and cleaning by removing stop words, punctuation, special characters, numbers, and white-spaces from reviews.
* Performed tokenization and stemming of reviews, and built a corpus out of it.
* Identified features of the restaurants from the reviews that customers had written using data mining and natural language processing.
* For each feature, opinion sentences were identified and categorized as positive or negative using the WordNet database.
* Produced a summary of the restaurant features based on the discovered information.
* Performed analysis and created intelligent dashboards using Tableau to discover top restaurants by positive and negative reviews, number of restaurants offering a specific cuisine, number of restaurants offering a specific feature/meal, number of restaurants by price category, top restaurants based on location, etc.
* Built a Flask application for users to search for restaurants based on their preferences – the application displays a feature based summary of reviews for the searched restaurant and provides restaurant statistics by city along with other key information.

### Code
1. [Restaurant Scraper](https://github.com/akshitvjain/restaurant-reviews/tree/master/restaurantscraper)
2. [Feature Review and Sentiment Analysis](https://github.com/akshitvjain/restaurant-reviews/blob/master/preprocess.py)
3. [Data Cleaning and Processing for Analysis](https://github.com/akshitvjain/restaurant-reviews/blob/master/analysis-rest.py)
4. [Web Application](https://github.com/akshitvjain/restaurant-reviews/tree/master/restaurantapp)

### Visualization
1. [UK Map - Filter by City/Price/Cuisine/Meal/Feature](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/FilterRestDashboard)
2. [Restaurant Statistics - Filter by City](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/RestaurantStatistics)
3. [Categorical/Positive/Negative Review Count - Filter by City](https://public.tableau.com/profile/akshit.jain6678#!/vizhome/RestaurantDataAnalysis/ReviewsDashboard)

### Screenshots (Restaurant App)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%203.40.00%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%203.40.39%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.04.56%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.05.07%20PM.png)
![link](https://github.com/akshitvjain/restaurant-reviews/blob/master/media/Screen%20Shot%202019-01-21%20at%204.05.27%20PM.png)

### Programming Language
Python

### Technologies
Scrapy, MongoDB, Flask

### Tools/IDE
Tableau, MacOS Terminal(Vim)
