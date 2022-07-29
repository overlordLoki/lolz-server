from itertools import combinations
import re
from numpy import True_
import pandas as pd
import betTypes as bt
import database as db

#fuction to for true or false if game is first in match
def isFirstOfMatch(df,i):
    return df['Num_in_Match'][i] == 1

#dataframe to check number of games in match
df_numInMatch = pd.read_sql_query('SELECT matchID, COUNT(matchID) FROM games GROUP BY matchID', db.engine)
#fuction to for true or false if game is last in match
def isLastOfMatch(df,i):
    matchID = df['matchID'][i]
    return df['Num_in_Match'][i] == df_numInMatch.loc[df_numInMatch['matchID'] == matchID].iloc[0,1]

#fuction to for true or false if game is 2ed in match
def isSecondOfMatch(df,i):
    return df['Num_in_Match'][i] == 2

#function to make all possible permutations of a list
def makeCombonations(input):
    return sum((list(map(list, combinations(input, i))) for i in range(len(input) + 1)), [])

#function to check boolen keys
def isSkipKey(df, keys, banList,i,num):
    #check if game is first in match
    if('banList' in keys):
        blueteam = df['Blue_Team_Name'][i]
        redteam = df['Red_Team_Name'][i]
        if (blueteam in banList) or (redteam in banList):
            return 1
    #first of match key
    if ('isFirstOfMatch' in keys) and not (isFirstOfMatch(df, i)):
        return 1
    #is last of match key
    if('isLastOfMatch' in keys) and not (isLastOfMatch(df, i)):
        return 1
    #is second of match key
    if('isSecondOfMatch' in keys) and not (isSecondOfMatch(df, i)):
        return 1
    #is not first of match key
    if('isNotFirstOfMatch' in keys) and isFirstOfMatch(df, i):
        return 1
    #is avg total kills less than num
    if('AvgTotalKillsLessThan' in keys) and not (isAvgTotalKillsLessThan(df, i, num)):
        return 1
    return 0

#if avg total kills is less than a given number, then bet on it
def isAvgTotalKillsLessThan(df, i, num):
    return (df['Total_kills'][:i].mean()) >= num


#helper functions

#function to set default values
def setDefults():
    units = 100.0
    wins = 0
    loses = 0     
    unitsOvertime = [units]
    return units,wins,loses,unitsOvertime

# fuction to do the bet
def makeBet(i, df, choice, num, betType):
    #do the bet
    if (betType == 'kills'):
        return bt.killsBet(i, df, choice, num)
    elif betType == 'dragons':
        return bt.dragonsBet(i, df, choice, num)
    elif betType == 'barons':
        return bt.baronsBet(i, df, choice, num)
    elif betType == 'towers':
        return bt.towerBet(i, df, choice, num)
    else:
        return bt.gameTimeBet(i, df, choice, num)

#function to do the bet
def doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i):
    #do the bet 
    outcome = makeBet(i, df, choice, num, betType)
    #update units
    wins += outcome
    loses += 1 - outcome
    if(outcome == 1):
        units += getOdds(df, choice, num, betType)
    else:
        units -= 1
    unitsOvertime.append(units)
    return units, wins, loses, unitsOvertime

#get the odds of the bet
def getOdds(df, choice, num, betType):
    if(betType == 'kills'):
        return 0.83 #this is a fixed number
    if (betType == 'dragons'):
        return 0.5 if (choice == 'over') else 1.9 #needs to be calculated
    if(betType == 'barons'):
        return 0.5 #needs to be calculated
    if(betType == 'towers'):
        return 0.83 #this is a fixed number
    if(betType == 'gameTime'):
        return 0.83 #this is a fixed number
    return 0.83

#function to decide the number the booky makes
def decideNum(df, i, betType):
    #decide the number the booky makes
    #kill bet number
    if (betType == 'kills'):
        if i >= 5:
            if df['region'][i] == 'LPL':
                return 25.5
            if df['region'][i] == 'LCK':
                return 21.5
            if df['region'][i] == 'LCS':
                return 21.5
            if df['region'][i] == 'LEC':
                return 22.5
        return df['Total_kills'][:i].mean()
    #dragon bet number
    if (betType == 'dragons'):
        return 4.5
    if betType == 'barons':
        return 1.5 
    if betType == 'towers':
        return 11.5 
    if betType == 'gameTime':
        return 32.30 #needs to be calculated
    return 32.30

#if units is higher add to df, remove smallest unit row
def checkIfHigher(df, testUnits , testWins, testLoses, testbanlist, testUnitsOvertime,keylist,betType,choice):
    totalbets = testWins + testLoses
    winrate = round(testWins/totalbets,2)
    if len(df.index) < 10:
        df.loc[len(df)] = ([testUnits, testWins, testLoses,totalbets,winrate,testUnitsOvertime, testbanlist,keylist,betType,choice])
        df = df.sort_values('units',ascending=False)
        df = df.reset_index(drop=True)
        return df
    df = df.sort_values('units',ascending=False)
    for i in range(len(df)):
        if(df['units'][i] > testUnits):
            #add to df
            df.loc[len(df)] = ([testUnits, testWins, testLoses,totalbets,winrate,testUnitsOvertime, testbanlist,keylist,betType,choice])
            #remove smallest unit row
            df = df.sort_values('units',ascending=True)
            df = df.drop(df.index[0])
            df = df.sort_values('units',ascending=False)
            df = df.reset_index(drop=True)
            break
    return df
