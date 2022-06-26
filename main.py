from turtle import update
import pandas as pd
from sqlalchemy import create_engine
import webscraper as ws

#create the engine
engine = create_engine('sqlite:///lolz.db', echo=False)

def getLastGames(num, team, tournament):
    return pd.read_sql_query("SELECT * FROM " 
                            + tournament +
                            " WHERE Game_Name like " "'" + team + "'"
                             + " LIMIT " + str(num), engine)

def getTable(tournament):
    df = pd.read_sql_query("SELECT * FROM " + tournament, engine)
    #df index on col index
    df = df.set_index('index')
    return df 

def makeCSVs():
    linkList = []
    for link in linkList:
        #make the df by webscraping the tournament
        df = ws.scrapeTourn(link)
        #get the tournament name from df
        name = df.iloc[0]['Tournament']
        print(name+' scraped')
        df.to_csv(name + '.csv')

def updateCurrent():
    linkList = ['https://gol.gg/tournament/tournament-matchlist/LEC%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCS%20Summer%202022/'
                ]
    for link in linkList:
        #make the df by webscraping the tournament
        df = ws.scrapeTourn(link)
        #get the tournament name from df
        name = df.iloc[0]['Tournament'].replace(' ', '_')
        print(name+' scraped')
        df.to_sql(name, engine, if_exists='replace')
        print(name+' updated')
