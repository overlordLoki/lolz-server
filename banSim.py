import pandas as pd
import simFunctions as sim
import database as db

#function to get the best banList
def bestBanList(df ,choice,betType , keys):
    count =0
    #simulation of a betting strategy
    tournament_name = df['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = sim.makeCombonations(teamsList)
    units =100.0
    bestbanlist = []
    for banlist in banlistCombo:
        count += 1
        testUnits = 100
        testUnits = banSim(df, choice, betType, banlist, keys)
        if(testUnits > units):
            units = testUnits
            bestbanlist = banlist
    return bestbanlist, count

#run sim for getting best banlist
def banSim(df ,choice,betType , banList, keys):
    units, wins, loses, unitsOvertime = sim.setDefults()
    for i in range(len(df)):
        num = sim.decideNum(df, i, betType)
        #key checks
        if sim.isSkipKey(df, keys, banList,i,num) == 1:
            continue
        units, wins, loses, unitsOvertime = sim.doTheBet(df, choice, num, betType, units, wins, loses, unitsOvertime, i)
    return units