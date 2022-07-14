import pandas as pd
import database as db
from itertools import combinations
import betTypes as bt

#function to get the best banList simulation
def bestTeamSim(df_testing):
    #simulation of a beting strategy
    tournament_name = df_testing['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = makeCombos(teamsList)
    units =100.0
    wins = 0
    loses = 0
    bestbanlist = []
    bestunitsovertime = []
    for banlist in banlistCombo:
        testUnits = 100
        testWins = 0
        testLoses = 0
        testUnitsOvertime = []
        testUnits , testWins, testLoses, testUnitsOvertime = runSim(df_testing, 'under', 21.5, 'kills', banlist, keys = ['banList'])
        if(testUnits > units):
            units = testUnits
            wins = testWins
            loses = testLoses
            bestbanlist = banlist
            bestunitsovertime = testUnitsOvertime
    totalbets = wins + loses
    winrate = round(wins/totalbets,2)
    return bestbanlist, units , wins, loses, winrate, totalbets, bestunitsovertime

def makeCombos(input):
    return sum((list(map(list, combinations(input, i))) for i in range(len(input) + 1)), [])

def runSim(df ,choice,num,betType,banList, keys):
    units = 100.0
    wins = 0
    loses = 0
    unitsOvertime = [units]
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
        #check if no more units to bet
        if (units < 1):
            print(f'no more units left after {str(i)} games')
            return units , wins, loses

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
            return units , wins, loses

        #update units
        wins += outcome
        loses += 1 - outcome
        if(outcome == 1):
            units += 0.83
        else:
            units -= 1
        unitsOvertime.append(units)
    return units , wins, loses, unitsOvertime

#fuction to for true or false if game is first in match
def isFirstOfMatch(df,i):
    return df['Num_in_Match'][i] == 1