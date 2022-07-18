import pandas as pd
import database as db
import mysql.connector as mysql

db = mysql.connect(host='140.238.205.186', user='loki', passwd='Thethethe3!', database='lolz')


# fuction to generate odds
def oddsGen(df):
    # create a new column for odds
    df['odds'] = 1
    # loop through the dataframe
    for i in range(len(df)):
        # if the home team wins
        if df.iloc[i]['home_team'] > df.iloc[i]['away_team']:
            # set the odds to 1.5
            df.iloc[i]['odds'] = 1.5
        # if the away team wins
        elif df.iloc[i]['home_team'] < df.iloc[i]['away_team']:
            # set the odds to 1.5
            df.iloc[i]['odds'] = 1.5
        # if the home team wins
        elif df.iloc[i]['home_team'] == df.iloc[i]['away_team']:
            # set the odds to 1.5
            df.iloc[i]['odds'] = 1.5
    # return the dataframe
    return df

# fuction to add a row to the mysql database
def insertOddsGame(df):
    mycursor = db.cursor()
    query = makequeryodds(df)
    mycursor.execute(query)
    return 0

#make a query to add a row to the mysql database
def makequeryodds(df):
    query = "INSERT INTO oddsTable (gameID,kills_num, kills_odds) VALUES ("
    val = ()
    return query, val

# fuction to calculate the num for kills
def killsNum(df):
    #get the teams playing

    return 21.5
    
# fuction to calculate the odds for kills
def killsOdds(df):
    #get the teams playing
    return 1.83