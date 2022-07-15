import re
import pandas as pd
import database as db
from itertools import combinations
import betTypes as bt

#function to run the sim
def runSim(df ,choice,num,betType , keys):
    units, wins, loses, unitsOvertime , banList = setDefults()
    #team ban list key
    if('banList' in keys):
        banList = bestBanList(df, choice, num, betType, keys)
    for i in range(len(df)):
        #key checks
        #team ban list key
        if('banList' in keys):
            blueteam = df['Blue_Team_Name'][i]
            redteam = df['Red_Team_Name'][i]
            if (blueteam in banList) or (redteam in banList):
                continue
        #first of match key
        if ('isFirstOfMatch' in keys) and not (isFirstOfMatch(df, i)):
            continue
        #is last of match key
        if('isLastOfMatch' in keys) and not (isLastOfMatch(df, i)):
            continue
        #is second of match key
        if('isSecondOfMatch' in keys) and not (isSecondOfMatch(df, i)):
            continue
        #check if no more units to bet
        if (units < 1):
            return units , wins, loses,banList, unitsOvertime

        #do the bet 
        if(betType == 'kills'):
            outcome = bt.killsBet(i, df, choice, num)
        elif(betType == 'dragons'):
            outcome = bt.dragonsBet(i, df, choice, num)
        elif(betType == 'barons'):
            outcome = bt.baronsBet(i, df, choice, num)
        elif(betType == 'tower'):
            outcome = bt.towerBet(i, df, choice, num)
        elif(betType == 'time'):
            outcome = bt.gameTimeBet(i, df, choice, num)
        else:
            print('invalid bet type')
            return units , wins, loses,banList, unitsOvertime

        #update units
        wins += outcome
        loses += 1 - outcome
        if(outcome == 1):
            units += 0.83
        else:
            units -= 1
        unitsOvertime.append(units)
    return units , wins, loses,banList, unitsOvertime


#function to get the best banList
def bestBanList(df ,choice,num,betType , keys):
    #simulation of a beting strategy
    tournament_name = df['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = makeCombonations(teamsList)
    units =100.0
    bestbanlist = []
    for banlist in banlistCombo:
        testUnits = 100
        testUnits = banSim(df, choice, num, betType, banlist, keys)
        if(testUnits > units):
            units = testUnits
            bestbanlist = banlist
    return bestbanlist

#run sim for getting best banlist
def banSim(df ,choice,num,betType , banList, keys):
    units, wins, loses, unitsOvertime , banlist = setDefults()
    for i in range(len(df)):
        #check ban list
        blueteam = df['Blue_Team_Name'][i]
        redteam = df['Red_Team_Name'][i]
        if (blueteam in banList) or (redteam in banList):
            continue
        #key checks
        #first of match key
        if ('isFirstOfMatch' in keys) and not (isFirstOfMatch(df, i)):
            continue
        #is last of match key
        if('isLastOfMatch' in keys) and not (isLastOfMatch(df, i)):
            continue
        #is second of match key
        if('isSecondOfMatch' in keys) and not (isSecondOfMatch(df, i)):
            continue
        #check if no more units to bet
        if (units < 1):
            print(f'no more units left after {str(i)} games')
            return units

        #do the bet 
        if(betType == 'kills'):
            outcome = bt.killsBet(i, df, choice, num)
        elif(betType == 'dragons'):
            outcome = bt.dragonsBet(i, df, choice, num)
        elif(betType == 'barons'):
            outcome = bt.baronsBet(i, df, choice, num)
        elif(betType == 'tower'):
            outcome = bt.towerBet(i, df, choice, num)
        elif(betType == 'time'):
            outcome = bt.gameTimeBet(i, df, choice, num)
        else:
            print('invalid bet type')
            return units

        #update units
        wins += outcome
        loses += 1 - outcome
        if(outcome == 1):
            units += 0.83
        else:
            units -= 1
        unitsOvertime.append(units)
    return units

#function to get the best key combinations
def bestKeysSim(df_testing, keys):
    #set starting values
    units, wins, loses, bestunitsovertime , bestbanlist = setDefults()
    bestKeySet = []
    keysCombo = makeCombonations(keys)
    for keylist in keysCombo:
        testUnits = 100
        testWins = 0
        testLoses = 0
        testUnitsOvertime = []
        testbanlist = []
        #units , wins , loses , banList, bestunitsovertime
        testUnits , testWins, testLoses, testbanlist, testUnitsOvertime = runSim(df_testing, 'under', 21.5, 'kills', keylist )
        if(testUnits > units):
            units = testUnits
            wins = testWins
            loses = testLoses
            bestbanlist = testbanlist
            bestunitsovertime = testUnitsOvertime
            bestKeySet = keylist
        
    totalbets = wins + loses
    winrate = round(wins/totalbets,2)
    return units , wins, loses, winrate, bestbanlist, totalbets, bestunitsovertime, bestKeySet


#helper functions

#function to set default values
def setDefults():
    units = 100.0
    wins = 0
    loses = 0     
    unitsOvertime = [units]
    banList = []
    return units,wins,loses,unitsOvertime, banList

#fuction to for true or false if game is first in match
def isFirstOfMatch(df,i):
    return df['Num_in_Match'][i] == 1

#fuction to for true or false if game is last in match
def isLastOfMatch(df,i):
    return df['Num_in_Match'][i] == df['Num_Games_in_Match'][i]

#fuction to for true or false if game is 2ed in match
def isSecondOfMatch(df,i):
    return df['Num_in_Match'][i] == 2

#function to make all possible permutations of a list
def makeCombonations(input):
    return sum((list(map(list, combinations(input, i))) for i in range(len(input) + 1)), [])