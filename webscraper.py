from ast import If
from calendar import c
import pandas as pd
from bs4 import BeautifulSoup
import requests
import scrapGame
import mysql.connector as mysql

db = mysql.connect(host='localhost', user='root', passwd='root', database='lolz')
mycursor = db.cursor()

def scrapeTourn(url,tournID):  # sourcery skip: for-append-to-extend, list-comprehension
    #link to the page
    source = requests.get(url , headers = {'User-agent': 'your bot 0.1'}).text
    #souping the page
    soup = BeautifulSoup(source, 'lxml')
    #make a list of all the match links
    links = []
    for link in soup.find_all('td', class_='text-left'):
        #if link.find('a') is not None:
        if link.find('a') is not None:
            #get the link
            li = link.find('a').get('href')
            #remove the first 2 char in each link
            li = li[2:]
            #add the link to the list
            links.append(li)
    #reverse the list so the most recent game is first
    links = links[::-1]
    #number of games currently in the tournament
    num_in_tourn = 1
    #dataframe to store the games
    cols = ['ID','MatchID', 'tournamentID','Game_Name','Match_Name', 'Tournament','Region','Num_in_Match', 
            'Blue_Team_Name','Red_Team_Name', 'Date', 'Week', 'Winner',
            'Blue_kills', 'Red_kills', 'Total_kills', 'Blue_towers', 'Red_towers', 'Total_towers',
            'Blue_dragons', 'Red_dragons', 'Total_dragons', 'Blue_barons', 'Red_barons', 'Total_barons',
            'Blue_gold', 'Red_gold', 'Total_gold', 'First_blood_team', 'First_blood_time', 'First_tower_team',
            'First_tower_time', 'First_dragon_team', 'First_dragon_time', 'First_rift_herald_team', 'First_rift_herald_time',
            'First_baron_team', 'First_baron_time', 'Game_time','Blue_players', 'Red_players']      
    #create the dataframe
    df = pd.DataFrame(columns = cols)
    df = scrapMatchs(links, num_in_tourn, df,tournID)
    return df

def scrapMatchs(links, num_in_tourn, df,tournID):
    num_of_match_in_tourn = 1;
    #for each link in the list, scrape the page building a match
    for link in links:
        if('page-preview' in link):
            continue
        URL = "https://gol.gg"+link;
        source = requests.get(URL, headers = {'User-agent': 'your bot 0.1'}).text
        soup = BeautifulSoup(source, 'lxml')
        #get the Match Name
        matchName = soup.find('div', class_='col-12 mt-4').find('h1').text
        #find nav class "class="navbar navbar-expand-md navbar-dark gamemenu""
        menu = soup.find('nav', class_ = 'navbar navbar-expand-md navbar-dark gamemenu').find_all('a')[1:-1]
        gamelinks = []
        region, tourmament = regionAndTourn(soup)
        matchID = matchIDMaker(tourmament, num_of_match_in_tourn)
        #if doesMatchExist(matchID): then continue
        if(doesMatchExist(matchID)):
            continue
        #if URl contains 'summary' then use makeMatchData else use makeMatchDataNoSum
        if('summary' in link):
            Qmatch = makeMatchData(num_in_tourn, tournID, num_of_match_in_tourn, soup, matchName, menu, gamelinks)
        else:
            Qmatch = makeMatchDataNoSum(num_in_tourn, tournID, num_of_match_in_tourn, soup, matchName, menu, gamelinks)
        mycursor.execute(Qmatch)
        print('Match inserted')
        num_of_match_in_tourn = num_of_match_in_tourn + 1
        #for each game in the match
        num_of_match = 1
        for game_link in gamelinks:
            game = scrapGame.scrapeGame(game_link,num_in_tourn,tournID,num_of_match,matchName,matchID)
            num_in_tourn += 1
            df = pd.concat([df,game], ignore_index=True)
            num_of_match += 1
            Qgame = QAddGame(game)
            mycursor.execute(Qgame)
            print('Game inserted')
    db.commit()
    print('committed')
    return df

def QAddGame(df):
    Q = ('INSERT INTO games (gameID, matchID,tournamentID, matchName,tournament_name, region,'
        ' Num_in_Match, Blue_Team_Name, Red_Team_Name, Date, Week, Winner, Blue_kills, Red_kills,'
        ' Total_kills, Blue_towers, Red_towers, Total_towers, Blue_dragons, Red_dragons, Total_dragons,'
        ' Blue_barons, Red_barons, Total_barons, Blue_gold, Red_gold, Total_gold, First_blood_team,'
        ' First_blood_time, First_tower_team, First_tower_time, First_dragon_team, First_dragon_time,'
        ' First_rift_herald_team, First_rift_herald_time, First_baron_team, First_baron_time, Game_time,'
        ' Blue_players, Red_players) VALUES ')
    values = queryGameValues(df)
    return Q+values

def queryGameValues(df):
    return ('('+str(df.iloc[0]['ID'])+','+ str(df.iloc[0]['MatchID'])+','+ str(df.iloc[0]['tournamentID'])+',"'+ str(df.iloc[0]['Match_Name'])+'",'
        '"'+ str(df.iloc[0]['Tournament'])+'","'+ str(df.iloc[0]['Region'])+'",'+ str(df.iloc[0]['Num_in_Match'])+',"'+ str(df.iloc[0]['Blue_Team_Name'])+'",'
        '"'+ str(df.iloc[0]['Red_Team_Name'])+'","'+ str(df.iloc[0]['Date'])+'","'+ str(df.iloc[0]['Week'])+'","'+ str(df.iloc[0]['Winner'])+'",'
        ''+ str(df.iloc[0]['Blue_kills'])+','+ str(df.iloc[0]['Red_kills'])+','+ str(df.iloc[0]['Total_kills'])+','+ str(df.iloc[0]['Blue_towers'])+','
        ''+ str(df.iloc[0]['Red_towers'])+','+ str(df.iloc[0]['Total_towers'])+','+ str(df.iloc[0]['Blue_dragons'])+','+ str(df.iloc[0]['Red_dragons'])+','
        ''+ str(df.iloc[0]['Total_dragons'])+','+ str(df.iloc[0]['Blue_barons'])+','+ str(df.iloc[0]['Red_barons'])+','+ str(df.iloc[0]['Total_barons'])+','
        ''+ str(df.iloc[0]['Blue_gold'])+','+ str(df.iloc[0]['Red_gold'])+','+ str(df.iloc[0]['Total_gold'])+',"'+ str(df.iloc[0]['First_blood_team'])+'",'
        ''+ str(df.iloc[0]['First_blood_time'])+',"'+ str(df.iloc[0]['First_tower_team'])+'",'+ str(df.iloc[0]['First_tower_time'])+',"'+ str(df.iloc[0]['First_dragon_team'])+'",'
        ''+ str(df.iloc[0]['First_dragon_time'])+',"'+ str(df.iloc[0]['First_rift_herald_team'])+'",'+ str(df.iloc[0]['First_rift_herald_time'])+','
        '"'+ str(df.iloc[0]['First_baron_team'])+'",'+ str(df.iloc[0]['First_baron_time'])+','+ str(df.iloc[0]['Game_time'])+',"'+ str(df.iloc[0]['Blue_players'])+'",'
        '"'+ str(df.iloc[0]['Red_players'])+'")')

def makeMatchData(num_in_tourn, tournID, num_of_match_in_tourn, soup, matchName, menu, gamelinks):
    # sourcery skip: inline-immediately-returned-variable
    #remove first 2 char in each link and add to gamelinks
    for m in menu:
        m = m.get('href')
        m = m[2:]
        gamelinks.append(m)
    region, tourmament = regionAndTourn(soup)
    #game date
    date = soup.find('div', class_ = 'col-12 col-sm-5 text-right').text.split(' ')[0]
    #match id
    matchID = matchIDMaker(tourmament, num_of_match_in_tourn)
    #get blue and red team names
    both = soup.findAll('div', class_='col-4 col-sm-5 text-center')
    blueTeam = both[0].text
    redTeam = both[1].text
    teams = blueTeam + ',' + redTeam
    #make the match query
    Qmatch = ('INSERT INTO matchs (matchID,matchName, tournamentID, date, tournament_name,teams,region,num_in_tourn) VALUES ('
              ''+str(matchID)+',"'+str(matchName)+'",'+str(tournID)+',"'+str(date)+'","'+str(tourmament)+'","'+str(teams)+'","'+str(region)+'",'+str(num_in_tourn)+');')
    return Qmatch

def regionAndTourn(soup):
    #region and tourmament
    regionAndTourmament = soup.find('div', class_ = 'col-12 col-sm-7').text.split(' ')
    region,tourmament = tourmAndregion(regionAndTourmament)
    if('(WR)' in tourmament):
        tourmament = tourmament.replace('(WR)','')
        tourmament = tourmament[:-1]
    return region,tourmament

def makeMatchDataNoSum(num_in_tourn, tournID, num_of_match_in_tourn, soup, matchName, menu, gamelinks):
    # sourcery skip: inline-immediately-returned-variable
    #remove first 2 char in each link and add to gamelinks
    for m in menu:
        m = m.get('href')
        m = m[2:]
        gamelinks.append(m)
    region, tourmament = regionAndTourn(soup)
    #game date
    date = soup.find('div', class_ = 'col-12 col-sm-5 text-right').text.split(' ')[0]
    #match id
    matchID = matchIDMaker(tourmament, num_of_match_in_tourn)
    #get blue and red team names
    blueTeam = soup.find('div',class_ ='col-12 blue-line-header').text.split('-')[0].replace('\n','')[:-1]
    redTeam =  soup.find('div',class_ ='col-12 red-line-header').text.split('-')[0].replace('\n','')[:-1]
    teams = blueTeam + ',' + redTeam
    #make the match query
    Qmatch = ('INSERT INTO matchs (matchID,matchName, tournamentID, date, tournament_name,teams,region,num_in_tourn) VALUES ('
              ''+str(matchID)+',"'+str(matchName)+'",'+str(tournID)+',"'+str(date)+'","'+str(tourmament)+'","'+str(teams)+'","'+str(region)+'",'+str(num_in_tourn)+');')
    return Qmatch

def matchIDMaker(tourmament_name, num_of_match_in_tourn):
    #region number
    regNum = 0;
    if(tourmament_name.__contains__('LEC')):
        regNum = 1;
    elif(tourmament_name.__contains__('LCS')):
        regNum = 2;
    elif(tourmament_name.__contains__('LCK')):
        regNum = 3;
    elif(tourmament_name.__contains__('LPL')):
        regNum = 4;
    #number for spring, spring playoffs, summer, summer playoffs, MSI , Worlds
    tNum = 0;
    if (tourmament_name.__contains__('Spring')):
        tNum = 2 if (tourmament_name.__contains__('Playoffs')) else 1
    elif (tourmament_name.__contains__('Summer')):
        tNum = 4 if (tourmament_name.__contains__('Playoffs')) else 3
    elif(tourmament_name.__contains__('MSI')):
        tNum = 5;
    elif(tourmament_name.__contains__('Worlds')):
        tNum = 6;
    #number for the year
    yearNum = tourmament_name[-2:]
    #build id and return it
    s = str(num_of_match_in_tourn) + str(tNum) + str(regNum) + str(yearNum)
    return int(s)
    
def tourmAndregion(regionAndTourmament):
    region = regionAndTourmament[0][1:5]
    tourmament = region+ "_" + regionAndTourmament[1] + '_' + regionAndTourmament[2]
    if(regionAndTourmament[2] == 'Playoffs'):
        tourmament = tourmament + '_' + regionAndTourmament[3]
    #remove last element in list
    regionAndTourmament = regionAndTourmament[:-1]
    return region,tourmament

def doesMatchExist(matchID):
    db = mysql.connect(host='localhost', user='root', passwd='root', database='lolz')
    mycursor = db.cursor()
    mycursor.execute(f'SELECT count(*) FROM matchs WHERE matchID = {matchID}')
    res = mycursor.fetchone()
    mycursor = db.cursor()
    return res[0] != 0