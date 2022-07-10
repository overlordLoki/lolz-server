import pandas as pd
from sqlalchemy import create_engine
import webscraper as ws
import mysql.connector as mysql
#create the engine
#engine = create_engine('sqlite:///lolz.db', echo=False)
#old databases
#db = mysql.connect(host='localhost', user='root', passwd='root', database='lolz')
#connect to the database on server
db = mysql.connect(host='140.238.205.186', user='loki', passwd='Thethethe3!', database='lolz')
mycursor = db.cursor()

def getLastGames(num, team, tournament):
    return pd.read_sql_query("SELECT * FROM " 
                            + tournament +
                            " WHERE Game_Name like " "'" + team + "'"
                             + " LIMIT " + str(num), db)

def getTable(tournament):
    # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
    db = mysql.connect(host='140.238.205.186', user='loki', passwd='Thethethe3!', database='lolz')
    tournament = str(tournament)
    if type(tournament) == int:
        df = pd.read_sql_query(f'SELECT * FROM games WHERE tournamentID = "{tournament}"', db)
    else:
        df = pd.read_sql_query(f'SELECT * FROM games WHERE tournament_name = "{tournament}"', db)
    return df

def getTable1(table, cursor):
    if(table in ['tournaments','matchs','games']):
        df = pd.read_sql_query(f'SELECT * FROM lolz.{table}', db)
    return df


def updateCurrent():
    linkList = ['https://gol.gg/tournament/tournament-matchlist/LEC%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCS%20Summer%202022/'
                ]
    for link in linkList:
        ws.scrapeTourn(link)

#add tournament to database
def addTorn(tournamentID,tournament_name,year, region,):
    mycursor.execute('INSERT INTO tournaments (tournamentID,tournament_name, year,region) VALUES ('+
                     tournamentID+ ',' + '"' +tournament_name +'"'+ ',' + year + ',' + '"'+ region + '"'+')')
    db.commit()
    return 1

    
def doesMatchExist(matchID):
    mycursor.execute(f'SELECT count(*) FROM matchs WHERE matchID = {matchID}')
    res = mycursor.fetchone()
    mycursor = db.cursor()
    return res[0] != 0

def remakeData():
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%202022/',1)
    print('finished LCK Spring')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCK%20Spring%20Playoffs%202022/',2)
    print('finished LCK Spring Playoffs')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LPL%20Spring%202022/',3)
    print('finished LPL Spring')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LPL%20Spring%20Playoffs%202022/',4)
    print('finished LPL Spring Playoffs')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%202022/',5)
    print('finished LEC Spring')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%20Playoffs%202022/',6)
    print('finished LEC Spring Playoffs')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCS%20Spring%202022/',7)
    print('finished LCS Spring')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCS%20Spring%20Playoffs%202022/',8)
    print('finished LCS Spring Playoffs')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/MSI%202022/',9)
    print('finished MSI')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/',10)
    print('finished LCK Summer')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%202022/',11)
    print('finished LPL Summer')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LEC%20Summer%202022/',12)
    print('finished LEC Summer')
    ws.scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LCS%20Summer%202022/',13)
    print('finished LCS Summer')
    print('done')


def remakeTourns():
    addTorn('1','LCK_Spring_2022', '2022', 'LCK')
    addTorn('2','LCK_Spring_Playoffs_2022', '2022', 'LCK')
    addTorn('3','LPL_Spring_2022', '2022', 'LPL')
    addTorn('4','LPL_Spring_Playoffs_2022', '2022', 'LPL')
    addTorn('5','LEC_Spring_2022', '2022', 'LEC')
    addTorn('6','LEC_Spring_Playoffs_2022', '2022', 'LEC')
    addTorn('7','LCS_Spring_2022', '2022', 'LCS')
    addTorn('8','LCS_Spring_Playoffs_2022', '2022', 'LCS')
    addTorn('9','MSI_2022', '2022', 'MSI')
    addTorn('10','LCK_Summer_2022', '2022', 'LCK')
    addTorn('11','LPL_Summer_2022', '2022', 'LPL')
    addTorn('12','LEC_Summer_2022', '2022', 'LEC')
    addTorn('13','LCS_Summer_2022', '2022', 'LCS')
    print('done')

