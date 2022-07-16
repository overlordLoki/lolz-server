import database as db
import pandas as pd
import simFuctions as sim

#function to run the sim
def runSim(df ,choice,num,betType , keys):
    units, wins, loses, unitsOvertime , banList = sim.setDefults()
    #team ban list key
    banList = []
    count = 0
    if('banList' in keys):
        banList,count = bestBanList(df, choice, num, betType, keys)
    for i in range(len(df)):
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        #check if no more units to bet
        if (units < 1):
            return units , wins, loses,banList, unitsOvertime
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units , wins, loses,banList, unitsOvertime,count

#function to get the best key combinations
def bestKeysSim(df_testing, keys):
    count =0
    #set starting values
    units, wins, loses, bestunitsovertime , bestbanlist = sim.setDefults()
    bestKeySet = []
    keysCombo = sim.makeCombonations(keys)
    for keylist in keysCombo:
        count += 1
        testUnits = 100
        testWins = 0
        testLoses = 0
        testUnitsOvertime = []
        testbanlist = []
        #units , wins , loses , banList, bestunitsovertime
        testUnits , testWins, testLoses, testbanlist, testUnitsOvertime,addToCount = runSim(df_testing, 'under', 21.5, 'kills', keylist )
        count += addToCount
        if(testUnits > units):
            units = testUnits
            wins = testWins
            loses = testLoses
            bestbanlist = testbanlist
            bestunitsovertime = testUnitsOvertime
            bestKeySet = keylist
        
    totalbets = wins + loses
    winrate = round(wins/totalbets,2)
    return units , wins, loses, winrate, bestbanlist, totalbets, bestunitsovertime, bestKeySet, count

#keys functions

#function to get the best banList
def bestBanList(df ,choice,num,betType , keys):
    count =0
    #simulation of a beting strategy
    tournament_name = df['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = sim.makeCombonations(teamsList)
    units =100.0
    bestbanlist = []
    for banlist in banlistCombo:
        count += 1
        testUnits = 100
        testUnits = banSim(df, choice, num, betType, banlist, keys)
        if(testUnits > units):
            units = testUnits
            bestbanlist = banlist
    return bestbanlist, count

#run sim for getting best banlist
def banSim(df ,choice,num,betType , banList, keys):
    units, wins, loses, unitsOvertime , ignore_this = sim.setDefults()
    for i in range(len(df)):
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units

