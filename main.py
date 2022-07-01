import pandas as pd
from sqlalchemy import create_engine
import webscraper as ws
import mysql.connector as mysql
#create the engine
engine = create_engine('sqlite:///lolz.db', echo=False)
db = mysql.connect(host='localhost', user='root', passwd='root', database='lolz')
mycursor = db.cursor()

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


def updateCurrent():
    linkList = ['https://gol.gg/tournament/tournament-matchlist/LEC%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCS%20Summer%202022/'
                ]
    

#add tournament to database
def addTorn(tournamentID,tournament_name,year, region,):
    mycursor.execute('INSERT INTO tournaments (tournamentID,tournament_name, year,region) VALUES ('+
                     tournamentID+ ',' + '"' +tournament_name +'"'+ ',' + year + ',' + '"'+ region + '"'+')')
    db.commit()
    return 1

#query to to see if database contains the match id
def checkMatchID(matchID):
    Q = f"SELECT * FROM matchs WHERE matchID = {str(matchID)};"
    return mycursor.execute(Q).fetchall()
    
# isthere = checkMatchID(15022)
# print(isthere)
result = mycursor.execute('SELECT * FROM lolz.tournaments;')
print(result.fetchall())

#ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/MSI%202022/',9)

# addTorn('3','LPL_Spring_2022', '2022', 'LPL')
# addTorn('4','LPL_Spring_Playoffs_2022', '2022', 'LPL')
# addTorn('5','LEC_Spring_2022', '2022', 'LEC')
# addTorn('6','LEC_Spring_Playoffs_2022', '2022', 'LEC')
# addTorn('7','LCS_Spring_2022', '2022', 'LCS')
# addTorn('8','LCS_Spring_Playoffs_2022', '2022', 'LCS')
# addTorn('9','MSI_2022', '2022', 'MSI')
# addTorn('10','LCK_Summer_2022', '2022', 'LCK')
# addTorn('11','LPL_Summer_2022', '2022', 'LPL')
# addTorn('12','LEC_Summer_2022', '2022', 'LEC')
# addTorn('13','LCS_Summer_2022', '2022', 'LCS')
