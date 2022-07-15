import re
import pandas as pd
import database as db
from itertools import combinations
import betTypes as bt

#function to run the sim
def runSim(df ,choice,num,betType , keys):
    units, wins, loses, unitsOvertime , banList = setDefults()
    #team ban list key
    banList = []
    if('banList' in keys):
        banList = bestBanList(df, choice, num, betType, keys)
    for i in range(len(df)):
        #key checks
        if isSkipKey(df, keys, banList,i) == 1:
            continue
        #check if no more units to bet
        if (units < 1):
            return units , wins, loses,banList, unitsOvertime
        units, wins, loses, unitsOvertime = doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units , wins, loses,banList, unitsOvertime

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

#keys functions

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
    units, wins, loses, unitsOvertime , banlist_ignore = setDefults()
    for i in range(len(df)):
        #key checks
        if isSkipKey(df, keys, banList,i) == 1:
            continue
        units, wins, loses, unitsOvertime = doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units

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
def isSkipKey(df, keys, banList,i):
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
    return 0


#helper functions

#function to set default values
def setDefults():
    units = 100.0
    wins = 0
    loses = 0     
    unitsOvertime = [units]
    banList = []
    return units,wins,loses,unitsOvertime, banList

# fuction to do the bet
def makeBet(i, df, choice, num, betType):
    #do the bet
    if (betType == 'kills'):
        return bt.killsBet(i, df, choice, num)
    elif betType == 'dragons':
        return bt.dragonsBet(i, df, choice, num)
    elif betType == 'barons':
        return bt.baronsBet(i, df, choice, num)
    elif betType == 'tower':
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
        units += 0.83
    else:
        units -= 1
    unitsOvertime.append(units)
    return units, wins, loses, unitsOvertime