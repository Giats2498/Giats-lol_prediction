# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 23:43:52 2020

@author: Giats
"""

import requests
import json
import pandas as pd
import time


def get_stats(api_key, server, league_names): 
    df_final = pd.DataFrame()
    
    for league in league_names:
        
        #Summoner Names
        print(league+" Summoner Names "+server+" : Started")
        #get request till http response code is 200
        while True:
            players_req = requests.get('https://'+server+'.api.riotgames.com/lol/league/v4/'+league+'/by-queue/RANKED_SOLO_5x5?api_key='+api_key)
            if(players_req.status_code == 200):
                break
            else:
                #sleep for 1 min
                print("Sleeping for 1 min")
                time.sleep(60)
        players = json.loads(players_req.content)
        summoner_names = []
        for player in players['entries']:
            summoner_names.append(player['summonerName'])
            #200 names per league
            if(len(summoner_names) == 200):
                break
        print(league+" Summoner Names "+server+" : Done")
        
        #Account IDs
        print(league+" Account IDs "+server+" : Started")
        account_ids = []
        for summoner_name in summoner_names:
            #time sleep just to not get error 429
            time.sleep(0.1)
            #error value
            error = 0
            error_flag = False
            while True:
                account_id_req = requests.get('https://'+server+'.api.riotgames.com/lol/summoner/v4/summoners/by-name/'+summoner_name+'?api_key='+api_key)
                if(account_id_req.status_code == 200):
                    break
                else:
                    #sleep for 1 min
                    print("Sleeping for 1 min")
                    time.sleep(60)
                    error = error + 1
                #if error = 2 it might be an error so we must continue to next value
                if(error == 2):
                    error_flag = True
                    break
            if(error_flag != True):
                account_id = json.loads(account_id_req.content)
                account_ids.append(account_id['accountId'])
            print(league+" Account IDs "+server+" : "+str(len(account_ids))+" of "+str(len(summoner_names)))
        print(league+" Account IDs "+server+" : Done")
        
        #Games ID 
        print(league+" Game IDs "+server+" : Started")
        games_ids = []
        #index value just for printing
        i=0;
        for account_id in account_ids:
            time.sleep(0.1)
            #error value
            error = 0
            error_flag = False
            while True:
                account_history_req = requests.get('https://'+server+'.api.riotgames.com/lol/match/v4/matchlists/by-account/'+account_id+'?api_key='+api_key)
                if (account_history_req.status_code == 200):
                    break
                else:
                    #sleep for 1 min
                    print("Sleeping for 1 min")
                    time.sleep(60)
                    error = error + 1
                if(error == 2):
                    error_flag = True
                    break
            if(error_flag != True):  
                account_history = json.loads(account_history_req.content)
                for game in account_history['matches']:
                    games_ids.append(game['gameId'])
            print(league+" Games IDs "+server+" : "+str(i)+" of "+str(len(summoner_names)))
            i = i + 1
        print(league+" Game IDs "+server+" : Done")
        
        #Game Stats
        print(league+" Game Stats "+server+" : Started")
        games_stats = []
        #index value just for printing
        i=0;
        for game_id in games_ids:
            time.sleep(0.1)
            error = 0
            error_flag = False
            while True:
                game_stats_req = requests.get('https://'+server+'.api.riotgames.com/lol/match/v4/matches/'+str(game_id)+'?api_key='+api_key)
                if(game_stats_req.status_code == 200):
                    break
                elif (game_stats_req.status_code == 404): 
                    # data not found so we must continue to next game
                    error = 2
                else:
                    print("Sleeping for 1 min")
                    time.sleep(60)
                    error = error + 1
                if(error == 2):
                    error_flag = True
                    break
            if(error_flag !=  True):
                #Sometimes we dont get all the data..
                try:
                    game_stats = json.loads(game_stats_req.content)
                    #creating variables by stats
                    gameId = game_stats['gameId']
                    gameDuration = game_stats['gameDuration']
                    hasWon = game_stats['teams'][0]['win']
                    firstBlood = game_stats['teams'][0]['firstBlood']
                    firstTower = game_stats['teams'][0]['firstTower']
                    firstInhibitor = game_stats['teams'][0]['firstInhibitor']
                    firstBaron = game_stats['teams'][0]['firstBaron']
                    firstDragon = game_stats['teams'][0]['firstDragon']
                    firstRiftHerald = game_stats['teams'][0]['firstRiftHerald']
                    towerKillsBlue = game_stats['teams'][0]['towerKills']
                    inhibitorKillsBlue = game_stats['teams'][0]['inhibitorKills']
                    baronKillsBlue = game_stats['teams'][0]['baronKills']
                    dragonKillsBlue = game_stats['teams'][0]['dragonKills']
                    riftHeraldKillsBlue = game_stats['teams'][0]['riftHeraldKills']
                    towerKillsRed = game_stats['teams'][1]['towerKills']
                    inhibitorKillsRed = game_stats['teams'][1]['inhibitorKills']
                    baronKillsRed = game_stats['teams'][1]['baronKills']
                    dragonKillsRed = game_stats['teams'][1]['dragonKills']
                    riftHeraldKillsRed = game_stats['teams'][1]['riftHeraldKills']
                    killsBlue = 0
                    deathsBlue = 0
                    assistsBlue = 0
                    largestKillingSpreeBlue = 0
                    largestMultiKillBlue = 0
                    totalDamageDealtBlue = 0
                    totalDamageTakenBlue = 0
                    totalHealBlue = 0
                    visionScoreBlue = 0
                    goldEarnedBlue = 0
                    champLevelBlue = 0
                    killsRed = 0
                    deathsRed = 0
                    assistsRed = 0
                    largestKillingSpreeRed = 0
                    largestMultiKillRed = 0
                    totalDamageDealtRed = 0
                    totalDamageTakenRed = 0
                    totalHealRed = 0
                    visionScoreRed = 0
                    goldEarnedRed = 0
                    champLevelRed = 0
                    for player in game_stats['participants']:
                        if(player['stats']['participantId'] <= 5):
                            killsBlue = killsBlue + player['stats']['kills']
                            deathsBlue = deathsBlue + player['stats']['deaths']
                            assistsBlue = assistsBlue + player['stats']['assists']
                            largestKillingSpreeBlue = largestKillingSpreeBlue + player['stats']['largestKillingSpree']
                            largestMultiKillBlue = largestMultiKillBlue + player['stats']['largestMultiKill']
                            totalDamageDealtBlue = totalDamageDealtBlue + player['stats']['totalDamageDealt']
                            totalDamageTakenBlue = totalDamageTakenBlue + player['stats']['totalDamageTaken']
                            totalHealBlue = totalHealBlue + player['stats']['totalHeal']
                            visionScoreBlue = visionScoreBlue + player['stats']['visionScore']
                            goldEarnedBlue = goldEarnedBlue + player['stats']['goldEarned']
                            champLevelBlue = champLevelBlue + player['stats']['champLevel']
                        else:
                            killsRed = killsRed + player['stats']['kills']
                            deathsRed = deathsRed + player['stats']['deaths']
                            assistsRed = assistsRed + player['stats']['assists']
                            largestKillingSpreeRed = largestKillingSpreeRed + player['stats']['largestKillingSpree']
                            largestMultiKillRed = largestMultiKillRed + player['stats']['largestMultiKill']
                            totalDamageDealtRed = totalDamageDealtRed + player['stats']['totalDamageDealt']
                            totalDamageTakenRed = totalDamageTakenRed + player['stats']['totalDamageTaken']
                            totalHealRed = totalHealRed + player['stats']['totalHeal']
                            visionScoreRed = visionScoreRed + player['stats']['visionScore']
                            goldEarnedRed = goldEarnedRed + player['stats']['goldEarned']
                            champLevelRed = champLevelRed + player['stats']['champLevel']
                    games_stats.append({
                            'gameId': gameId,'gameDuration': gameDuration,'hasWon': hasWon,'firstBlood': firstBlood,
                            'firstTower': firstTower,'firstInhibitor': firstInhibitor,'firstBaron': firstBaron,'firstDragon': firstDragon,
                            'firstRiftHerald': firstRiftHerald,'towerKillsBlue': towerKillsBlue,'inhibitorKillsBlue': inhibitorKillsBlue,
                            'baronKillsBlue': baronKillsBlue,'dragonKillsBlue': dragonKillsBlue,'riftHeraldKillsBlue': riftHeraldKillsBlue,
                            'towerKillsRed': towerKillsRed,'inhibitorKillsRed': inhibitorKillsRed,'baronKillsRed': baronKillsRed,
                            'dragonKillsRed': dragonKillsRed,'riftHeraldKillsRed': riftHeraldKillsRed,'killsBlue': killsBlue,
                            'deathsBlue': deathsBlue,'assistsBlue': assistsBlue,'largestKillingSpreeBlue':largestKillingSpreeBlue,
                            'largestMultiKillBlue': largestMultiKillBlue,'totalDamageDealtBlue': totalDamageDealtBlue,
                            'totalDamageTakenBlue':totalDamageTakenBlue,'totalHealBlue':totalHealBlue,'visionScoreBlue':visionScoreBlue,
                            'goldEarnedBlue':goldEarnedBlue,'champLevelBlue':champLevelBlue,'killsRed': killsRed,
                            'deathsRed': deathsRed,'assistsRed': assistsRed,'largestKillingSpreeRed':largestKillingSpreeRed,
                            'largestMultiKillRed': largestMultiKillRed,'totalDamageDealtRed': totalDamageDealtRed,
                            'totalDamageTakenRed':totalDamageTakenRed,'totalHealRed':totalHealRed,'visionScoreRed':visionScoreRed,
                            'goldEarnedRed':goldEarnedRed,'champLevelRed':champLevelRed
                    })
                except Exception:
                    print("Continuing to next game..")
                    pass
            print(league+" Games Stats "+server+ " : "+str(i)+" of "+str(len(games_ids)))
            i = i + 1
        print(league+" Game Stats "+server+" : Done")
        df = pd.DataFrame(games_stats)
        df_final = df_final.append(df)
    df_final.to_csv("lol_games.csv",  index=False)