import pandas as pd

# fuction to do a tower bet
def towerBet(gameNum, df, underOrOver, towerNum):
    game = df.iloc[gameNum]
    return 1 if (
            underOrOver == 'under') and (game['Total_towers'] > towerNum) or (
            underOrOver != 'under' and (game['Total_towers'] < towerNum)) else 0
            
# fuction to do a dragon bet
def dragonsBet(gameNum, df, underOrOver, dragonNum):
    game = df.iloc[gameNum]
    return 1 if (
            underOrOver == 'under') and (game['Total_dragons'] > dragonNum) or (
            underOrOver != 'under' and (game['Total_dragons'] < dragonNum)) else 0

# fuction to do a kills bet
def killsBet(gameNum, df, underOrOver, killsNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Total_kills'] > killsNum) or (
        underOrOver != 'under' and (game['Total_kills'] < killsNum)) else 0

# fuction to do a barons bet
def baronsBet(gameNum, df, underOrOver, baronNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Total_barons'] > baronNum) or (
        underOrOver != 'under' and (game['Total_barons'] < baronNum)) else 0

# fuction to do a game time bet
def gameTimeBet(gameNum, df, underOrOver, timeNum):
    game = df.iloc[gameNum]
    return 1 if (
        underOrOver == 'under') and (game['Game_time'] > timeNum) or (
        underOrOver != 'under' and (game['Game_time'] < timeNum)) else 0