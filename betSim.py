import pandas as pd

def towerBet(gameNum, df, underOrOver, towerNum):
    game = df.iloc[gameNum]
    return 1 if (underOrOver == 'under') and (game['Total_towers'] > towerNum) or underOrOver != 'under' and (game['Total_towers'] < towerNum) else 0

def dragonsBet(gameNum, df, underOrOver, dragonNum):
    game = df.iloc[gameNum]
    return 1 if (underOrOver == 'under') and (game['Total_dragons'] > dragonNum) or underOrOver != 'under' and (game['Total_dragons'] < dragonNum) else 0

def killsBet(gameNum, df, underOrOver, killsNum):
    game = df.iloc[gameNum]
    return 1 if (underOrOver == 'under') and (game['Total_kills'] > killsNum) or underOrOver != 'under' and (game['Total_kills'] < killsNum) else 0

def baronsBet(gameNum, df, underOrOver, baronNum):
    game = df.iloc[gameNum]
    return 1 if (underOrOver == 'under') and (game['Total_barons'] > baronNum) or underOrOver != 'under' and (game['Total_barons'] < baronNum) else 0

def gameTimeBet(gameNum, df, underOrOver, timeNum):
    game = df.iloc[gameNum]
    return 1 if (underOrOver == 'under') and (game['Game_time'] > timeNum) or underOrOver != 'under' and (game['Game_time'] < timeNum) else 0

