import pandas as pd
import database as db
from itertools import combinations

def towerBet(gameNum, df, underOrOver, towerNum):
    game = df.iloc[gameNum]
    return 1 if (
            underOrOver == 'under') and (game['Total_towers'] > towerNum) or (
            underOrOver != 'under' and (game['Total_towers'] < towerNum)) else 0

def dragonsBet(gameNum, df, underOrOver, dragonNum):
    game = df.iloc[gameNum]
    return 1 if (
            underOrOver == 'under') and (game['Total_dragons'] > dragonNum) or (
            underOrOver != 'under' and (game['Total_dragons'] < dragonNum)) else 0

def killsBet(gameNum, df, underOrOver, killsNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Total_kills'] > killsNum) or (
        underOrOver != 'under' and (game['Total_kills'] < killsNum)) else 0

def baronsBet(gameNum, df, underOrOver, baronNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Total_barons'] > baronNum) or (
        underOrOver != 'under' and (game['Total_barons'] < baronNum)) else 0

def gameTimeBet(gameNum, df, underOrOver, timeNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Game_time'] > timeNum) or (
        underOrOver != 'under' and (game['Game_time'] < timeNum)) else 0

def bestTeamSim(df_testing):
    #simulation of a beting strategy
    tournament_name = df_testing['tournament_name'][0]
    teamsList = db.getTeamNames(tournament_name)
    banlistCombo = makeCombos(teamsList)
    units =100.0
    wins = 0
    loses = 0
    bestbanlist = []
    for banlist in banlistCombo:
        testUnits = 100
        testWins = 0
        testLoses = 0
        testUnits , testWins, testLoses = runSim(df_testing, 'under', 21.5, 'kills', banlist)
        if(testUnits > units):
            units = testUnits
            wins = testWins
            loses = testLoses
            bestbanlist = banlist
    totalbets = wins + loses
    winrate = round(wins/totalbets,2)
    return bestbanlist, units , wins, loses, winrate, totalbets

def makeCombos(input):
    return sum((list(map(list, combinations(input, i))) for i in range(len(input) + 1)), [])

def runSim(df ,choice,num,betType,banList):
    units = 100.0
    wins = 0
    loses = 0
    for i in range(len(df)):
        blueteam = df['Blue_Team_Name'][i]
        redteam = df['Red_Team_Name'][i]
        if (blueteam in banList) or (redteam in banList):
            continue
        if (units < 1):
            print(f'no more units left after {str(i)} games')
            return units , wins, loses
        if(betType == 'kills'):
            outcome = killsBet(i, df, choice, num)
        elif(betType == 'dragons'):
            outcome = dragonsBet(i, df, choice, num)
        elif(betType == 'barons'):
            outcome = baronsBet(i, df, choice, num)
        elif(betType == 'tower'):
            outcome = towerBet(i, df, choice, num)
        elif(betType == 'time'):
            outcome = gameTimeBet(i, df, choice, num)
        else:
            print('invalid bet type')
            return units , wins, loses
        wins += outcome
        loses += 1 - outcome
        if(outcome == 1):
            units += 0.83
        else:
            units -= 1
    return units , wins, loses