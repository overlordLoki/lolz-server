#this file is for calling premade meatheds for the database
import pandas as pd
import sqlalchemy as sql
import webscraper as ws
import mysql.connector as mysql
import passwords as pw

password = pw.getLogin()
ip = pw.getIP()
db = mysql.connect(host= ip, user='loki', passwd=password, database='lolz')
mycursor = db.cursor()
engine = sql.create_engine(
    'mysql+mysqlconnector://loki:'+password+'@'+ip+'/lolz',
    connect_args= dict(host= ip, port=3306))

#get the table from the database
def getTable(tournament):
    # sourcery skip: assign-if-exp, inline-immediately-returned-variable, lift-return-into-if
    db = mysql.connect(host='140.238.205.186', user='loki', passwd='Thethethe3!', database='lolz')
    tournament = str(tournament)
    if type(tournament) == int:
        df = pd.read_sql_query(f'SELECT * FROM games WHERE tournamentID = "{tournament}"', engine)
    else:
        df = pd.read_sql_query(f'SELECT * FROM games WHERE tournament_name = "{tournament}"', engine)
    return df

def getTable1(table, db):
    if(table in ['tournaments','matchs','games']):
        df = pd.read_sql_query(f'SELECT * FROM lolz.{table}', engine)
    return df

def getRecentGames(team, tournament, num):
    query = ('SELECT * FROM games ' +
          'WHERE matchname LIKE "' + '%' + team + '%" AND tournament_name = ' + '"' + tournament + '" ' 
          +'LIMIT ' + str(num))
    return pd.read_sql_query(query, engine)

def getTeamLast5Games(team):
    query = ('SELECT * FROM games ' +
          'WHERE matchname LIKE "' + '%' + team + '%"  LIMIT 5')
    return pd.read_sql_query(query, engine)

def getTournaments():
    query = 'SELECT * FROM tournaments'
    return pd.read_sql_query(query, engine)

#get team names given a tournament name
def getTeamNames(tournament):
    df = getTable(tournament)
    blue = df['Blue_Team_Name'].unique()
    red = df['Red_Team_Name'].unique()
    return list({*blue, *red})


def updateCurrent():
    linkList = ['https://gol.gg/tournament/tournament-matchlist/LCK%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LPL%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LEC%20Summer%202022/',
                'https://gol.gg/tournament/tournament-matchlist/LCS%20Summer%202022/'
                ]
    for NUM, link in enumerate(linkList, start=10):
        ws.scrapeTourn(link,NUM)
    

#add tournament to database
def addTorn(tournamentID,tournament_name,year, region,):
    mycursor.execute('INSERT INTO tournaments (tournamentID,tournament_name, year,region) VALUES ('+
                     tournamentID+ ',' + '"' +tournament_name +'"'+ ',' + year + ',' + '"'+ region + '"'+')')
    db.commit()
    return 1

#does match exist in database
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

