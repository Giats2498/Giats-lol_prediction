# -*- coding: utf-8 -*-
"""
Created on Sat May  2 02:05:26 2020

@author: Giats
"""

# Import libraries for machine learning models
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

import pandas as pd
import numpy as np

print('Machine Learning Libraries Imported!')

df = pd.read_csv("data_cleaned.csv")


# Seperate dependent variable from dataframe
y = df.hasWon

# Seperate independent variable from dataframe
x = df.drop('hasWon', axis =1)

#normalize the features
sc = StandardScaler()
X = sc.fit(x).transform(x.astype(float))

# train test split 
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)
print ('Train set:', X_train.shape,  y_train.shape)
print ('Test set:', X_test.shape,  y_test.shape)

# import prettytable for outputs of our models
from prettytable import PrettyTable
table = PrettyTable()
table.field_names = ['Algorithm', 'Accuracy', 'Recall', 'Precision', 'F-Score']


# K-Nearest Neighbours
# Test different values of k
Ks = 10
mean_acc = np.zeros((Ks-1))
for n in range(1,Ks):
    kneigh = KNeighborsClassifier(n_neighbors = n).fit(X_train,y_train)
    y_pred = kneigh.predict(X_test)
    mean_acc[n-1] = metrics.accuracy_score(y_test, y_pred)

# Use most accurate k value to predict test values
k = mean_acc.argmax()+1
neigh = KNeighborsClassifier(n_neighbors = n).fit(X_train,y_train)
y_pred = neigh.predict(X_test)

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'K-Nearest Neighbours'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])
    

    
#Decision Trees
# Initialise Decision Tree classifier and predict
drugTree = DecisionTreeClassifier(criterion="entropy", max_depth = 4)
drugTree.fit(X_train,y_train)
y_pred = drugTree.predict(X_test)

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'Decision Trees'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])



#Logistic Regression
# Train and predict logistic regression model
LR = LogisticRegression(C=0.01, solver='liblinear')
y_pred = LR.fit(X_train,y_train).predict(X_test)

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'Logistic Regression'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)    

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])
    
    
#Support Vector Machines
clf = svm.SVC(kernel='rbf')
y_pred = clf.fit(X_train, y_train).predict(X_test)

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'Support Vector Machines'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])
    

#Naive Bayes 
gnb = GaussianNB()
y_pred = gnb.fit(X_train, y_train).predict(X_test)  

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'Naive Bayes'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)  

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])
    
    

#Random Forest
# Instantiate Random Forest Classifier and predict values
clf = RandomForestClassifier(max_depth=2, random_state=0)
y_pred = clf.fit(X_train, y_train).predict(X_test)

# Create confusion matrix and interpret values
con = confusion_matrix(y_test, y_pred)
tp, fn, fp, tn = con[0][0], con[0][1], con[1][0], con[1][1]
algorithm = 'Random Forest Classifier'
accuracy = (tp + tn) / (tp + tn + fp + fn)
recall = tp / (tp + fn)
precision = tp / (tp + fp)
f_score = (2 * precision * recall) / (recall + precision)

# Add values to table
table.add_row([algorithm, round(accuracy,5), round(recall,5),
               round(precision,5), round(f_score,5)])
    
    
#Print Stats of models
print(table)

#GridSearchCV for SVC
from sklearn.model_selection import GridSearchCV
param_grid = {'C': [0.1,1, 10, 100], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf']}
gs = GridSearchCV(svm.SVC(),param_grid,refit=True,verbose=2)
gs.fit(X_train,y_train)

print(gs.best_score_)
print(gs.best_estimator_)

#create model file
import pickle
pickl = {'model': gs.best_estimator_}
pickle.dump( pickl, open( 'model_file' + ".p", "wb" ))

#create standard scaler file
pickle.dump(sc, open('scaler.pkl','wb'))
