# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 16:03:50 2020

@author: Giats
"""

import pandas as pd

df = pd.read_csv("lol_games.csv")

#drop game id column
df = df.drop(['gameId'], axis=1)

#Win = 1 , Fail = 0 for hasWon column
df['hasWon'] = df['hasWon'].apply(lambda x: 1 if 'win' in x.lower() else 0)

#True = 1 , False = 0 for columns firstBlood,firstTower,firstInhibitor,firstBaron,firstDragon,firstRiftHerald
categories = ['hasWon', 'firstBlood', 'firstTower','firstBaron', 'firstDragon', 'firstInhibitor','firstRiftHerald']
for category in categories:
    df[category] = df[category].astype(int)

df.to_csv('data_cleaned.csv',index = False)