from click import command
import pandas as pd
from sqlalchemy import create_engine
import webscraper as ws

#load in the csv files
# lck_df = pd.read_csv('data/LCK Spring 2022.csv')
# lcs_df = pd.read_csv('data/LCS Spring 2022.csv')
# lpl_df = pd.read_csv('data/LPL Spring 2022.csv')
# lec_df = pd.read_csv('data/LEC Spring 2022.csv')
# lec_playoffs_df = pd.read_csv('data/LEC Spring Playoffs 2022.csv')
# lpl_playoffs_df = pd.read_csv('data/LPL Spring Playoffs 2022.csv')
# lcs_playoffs_df = pd.read_csv('data/LCS Spring Playoffs 2022.csv')
# lck_playoffs_df = pd.read_csv('data/LCK Spring Playoffs 2022.csv')
# msi_df = pd.read_csv('data/MSI 2022.csv')
#create the engine
engine = create_engine('sqlite:///lolz.db', echo=False)
#write the df to the sql as table 'LCK_Spring_2022'
# lck_df.to_sql('LCK_Spring_2022', engine, if_exists='replace', index=False)
# lpl_df.to_sql('LPL_Spring_2022', engine, if_exists='replace', index=False)
# lpl_playoffs_df.to_sql('LPL_Spring_Playoffs_2022', engine, if_exists='replace', index=False)
# lec_df.to_sql('LEC_Spring_2022', engine, if_exists='replace', index=False)
# lec_playoffs_df.to_sql('LEC_Spring_Playoffs_2022', engine, if_exists='replace', index=False)
# lcs_df.to_sql('LCS_Spring_2022', engine, if_exists='replace', index=False)
# lcs_playoffs_df.to_sql('LCS_Spring_Playoffs_2022', engine, if_exists='replace', index=False)
# lck_playoffs_df.to_sql('LCK_Spring_Playoffs_2022', engine, if_exists='replace', index=False)
# msi_df.to_sql('MSI_2022', engine, if_exists='replace', index=False)

# def makeCSVs():
#     linkList = ['https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%20Playoffs%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%20Playoffs%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LPL%20Spring%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LPL%20Spring%20Playoffs%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LCS%20Spring%202022/',
#             'https://gol.gg/tournament/tournament-matchlist/LCS%20Spring%20Playoffs%202022/'
#             ]
#     for link in linkList:
#         #make the df by webscraping the tournament
#         df = ws.scrapeTourn(link)
#         #get the tournament name from df
#         name = df.iloc[0]['Tournament']
#         print(name+' scraped')
#         df.to_csv(name + '.csv')
        