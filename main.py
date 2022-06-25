# sourcery skip: avoid-builtin-shadow
import re
from unittest import result
from click import command
from matplotlib.pyplot import get
import pandas as pd
from sqlalchemy import create_engine
import webscraper as ws

#load in the csv files
# lck_df = pd.read_csv('data/LCK_Spring_2022.csv')
# lcs_df = pd.read_csv('data/LCS_Spring_2022.csv')
# lpl_df = pd.read_csv('data/LPL_Spring_2022.csv')
# lec_df = pd.read_csv('data/LEC_Spring_2022.csv')
# lec_playoffs_df = pd.read_csv('data/LEC_Spring_Playoffs_2022.csv')
# lpl_playoffs_df = pd.read_csv('data/LPL_Spring_Playoffs_2022.csv')
# lcs_playoffs_df = pd.read_csv('data/LCS_Spring_Playoffs_2022.csv')
# lck_playoffs_df = pd.read_csv('data/LCK_Spring_Playoffs_2022.csv')
# msi_df = pd.read_csv('data/MSI_2022.csv')
# #add them a list
# list = [lck_df, lcs_df, lpl_df, lec_df, lec_playoffs_df, lpl_playoffs_df, lcs_playoffs_df, lck_playoffs_df, msi_df]
#create the engine
engine = create_engine('sqlite:///lolz.db', echo=False)

def getLastGames(num, team, tournament):
    return pd.read_sql_query("SELECT * FROM " 
                             + "'" + tournament + "'" +
                            " WHERE Game_Name like " "'" + team + "'"
                             + " LIMIT " + str(num), engine)

def getTable(tournament):
    return pd.read_sql_query("SELECT * FROM " + tournament, engine)

def makeCSVs():
    linkList = []
    for link in linkList:
        #make the df by webscraping the tournament
        df = ws.scrapeTourn(link)
        #get the tournament name from df
        name = df.iloc[0]['Tournament']
        print(name+' scraped')
        df.to_csv(name + '.csv')

# df = getLastGames(1, 'T1', 'LCK Spring 2022')
# print(df)