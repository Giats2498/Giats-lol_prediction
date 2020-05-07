# League of Legends Win Estimator: Project Overview 
* Created a tool that estimates League of Legends Win (Accuracy ~ 99.34%) to help players of this game when a match is still worth playing or to give up early.
* Scraped over 235K high elo matches ```Ranked-SOLO-5x5``` (Challenger,Grandmaster,Master) from servers EUNE, EUW, LAN , NA, TR, JP and KR using python and [Riot API](https://developer.riotgames.com/).
* Analysed and visualized almost all varriables using popular python's packages. 
* Optimized K-Nearest Neighbours, Decision Trees, Logistic Regression,  Support Vector Machines, Naive Bayes, and Random Forest Regressors using GridsearchCV to reach the best model. 
* Built a client facing API using flask 

## Code and Resources Used 
**Python Version:** 3.6  
**Packages:** pandas, numpy, prettytable, sklearn, matplotlib, seaborn, selenium, flask, json, pickle  
**For Web Framework Requirements:**  ```pip install -r requirements.txt```  
**Flask Productionization:** https://towardsdatascience.com/productionize-a-machine-learning-model-with-flask-and-heroku-8201260503d2

## Web Scraping
Used scraper to scrape 237.972 matches from high elo players in patch 10.8. With each match, we got the following:
* Game ID  
* Game Duration (in seconds)
*	Win* 
*	First Blood** 
*	First Inhibitor** 
*	First Baron**
*	First Rift Herald**
*	Towers Destroyed Blue
*	Inhibitors Destroyed Blue
*	Baron Kills Blue 
*	Dragons Kills Blue 
*	Rift Herald Kills Blue
*	Towers Destroyed Red
*	Inhibitors Destroyed Red
*	Baron Kills Red 
*	Dragons Kills Red 
*	Rift Herald Kills Red
*	Kills Blue
*	Deths Blue
*	Assists Blue
*	Largest Kill Spree Blue
*	Largest Multi Kill Blue
*	Total Damage Dealt Blue
*	Total Damage Taken Blue
*	Total Heal Blue
*	Vision Score Blue
*	Gold Earned Blue
* Champions' Level Blue
*	Kills Red
*	Deths Red
*	Assists Red
*	Largest Kill Spree Red
*	Largest Multi Kill Red
*	Total Damage Dealt Red
*	Total Damage Taken Red
*	Total Heal Red
*	Vision Score Red
*	Gold Earned Red
* Champions' Level Red

   *(True = Won Blue Side, False = Won Red Side)
   
   **(True = Blue Side Got it, False = Red Side Got it) 

## EDA Highlights
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/1.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/3.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/4.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/5.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/6.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/7.PNG)
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/8.PNG)

## Model Building - Model performance

First, I Standardized all the variables using sklearn StandardScaler, I also split the data into train and tests sets with a test size of 20%.   

I tried six different models, here is their stats:  
![alt text](https://github.com/Giats2498/Giats-lol_prediction/blob/master/images/stats.PNG)

After that i tried to use GridSearchCV on Support Vector Machines model:
* Best Estimator: SVC(C=100, break_ties=False, cache_size=200,class_weight=None,coef0=0.0,decision_function_shape='ovr',degree=3,gamma=0.01,kernel='rbf',
                max_iter=-1, probability= True, random_state= None, shrinking= True,tol=0.001, verbose=False)
* Best Score: 0.993423

## Productionization 
In this step, I built a flask API endpoint that was hosted on a local webserver by following along with the TDS tutorial in the reference section above. The API endpoint takes in a request with a list of values from a league of legends match and returns an estimated win side (1=Blue Side Win, 0 = Red Side Win). 
