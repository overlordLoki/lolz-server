from re import T
from bs4 import BeautifulSoup
import requests

def scrapeGame(link):
    URL = "https://gol.gg"+link;
    source = requests.get(URL, headers = {'User-agent': 'your bot 0.1'}).text
    soup = BeautifulSoup(source, 'lxml')
    
    elements = soup.find_all('div', class_ = 'col-cadre')
    #remove last 1 element
    elements = elements[:-1]
    elem = elements[0]
    
    #............................................................
    #game time
    #get game time "col-6 text-center"
    gametime = elements[0].find('div', class_ = 'col-6 text-center').text.split('\n')[1]
    
    #.............................................................
    #game date
    dateAndWeek = soup.find('div', class_ = 'col-12 col-sm-5 text-right').text.split(' ')
    date = dateAndWeek[0]
    week = dateAndWeek[1]
    #remove first 5 char in week and last char in week
    week = week[5:-1]
    week = int(week)
    
    #................................................................
    #blue team name and win/loss
    blueteambanner  = elem.find('div',class_ ='col-12 blue-line-header').text
    outcome = blueteambanner.split('-')[1]
    blueTeamName = blueteambanner.split('-')[0].replace('\n','')
    blueWin = False
    if(outcome == ' WIN'):
        blueWin = True
    
    #red team name and win/loss
    redteambanner = elem.find('div',class_ ='col-12 red-line-header').text
    outcome = redteambanner.split('-')[1]
    redTeamName = redteambanner.split('-')[0].replace('\n','')
    redWin = False
    if(outcome == ' WIN'):
        redWin = True
    
    #.............................................................
    #region and tourmament
    regionAndTourmament = soup.find('div', class_ = 'col-12 col-sm-7').text.split(' ')
    region = regionAndTourmament[0][1:5]
    tourmament = region+ " " + regionAndTourmament[1] + ' ' + regionAndTourmament[2]
    
    #.............................................................
    # both red and blue team stats boxs
    Teamstats = soup.find_all('div', class_ = 'col-12 col-sm-6')
    
    #blue team stats
    blueTeamStats = Teamstats[0].find_all('div', class_ = 'row')[1].find_all('div', class_ = 'col-2')
    #blue team kills
    blueKills = blueTeamStats[0].find('span', class_ = 'score-box blue_line').text.split(' ')[1]
    #first blood
    FB = blueTeamStats[0].find('img', alt = 'First Blood')
    blueFB = False
    if(FB != None):
        blueFB = True
    #blue towers
    blueTowers = blueTeamStats[1].find('span', class_ = 'score-box blue_line').text.split(' ')[1]
    #first tower
    FT = blueTeamStats[1].find('img', alt = 'First Tower')
    blueFT = False
    if(FT != None):
        blueFB = True
    #blue dragons
    blueDragons = blueTeamStats[2].find('span', class_ = 'score-box blue_line').text.split(' ')[1]
    #blue Barons
    blueBarons = blueTeamStats[3].find('span', class_ = 'score-box blue_line').text
    #blue Gold
    blueGold = blueTeamStats[4].find('span', class_ = 'score-box blue_line').text.split('k')[0].split(' ')[1]
    
    #....................................................................
    #red team stats
    redTeamScores = Teamstats[1].find_all('div', class_ = 'row')[1].find_all('div', class_ = 'col-2')
    #red kills
    redKills = redTeamScores[0].find('span', class_ = 'score-box red_line').text.split(' ')[1]
    #first blood
    FB = redTeamScores[0].find('img', alt = 'First Blood')
    redFB = False
    #check if FB is not None
    if(FB != None):
        redFB = True
    #red towers
    redTowers = redTeamScores[1].find('span', class_ = 'score-box red_line').text.split(' ')[1]
    #first tower
    FT = redTeamScores[1].find('img', alt = 'First Tower')
    redFT = False
    if(FT != None):
        redFT = True
    #number of dragons
    redDragons = redTeamScores[2].find('span', class_ = 'score-box red_line').text.split(' ')[1]
    #number of barons
    redBarons = redTeamScores[3].find('span', class_ = 'score-box red_line').text
    #number of gold
    redGold = redTeamScores[4].find('span', class_ = 'score-box red_line').text.split('k')[0].split(' ')[1]
    #......................................................................................................
    #table of players and items
    #get tables 'playersInfosLine footable toggle-square-filled'
    tables = soup.find_all('table', class_ = 'playersInfosLine footable toggle-square-filled')
    #get blue team players
    bluePlayers = []
    allPlayers =tables[0].find_all('tr')[1:]
    for player in allPlayers:
        bluePlayers += [player.find('a', class_ = 'link-blanc').text]

    #get red team players
    redPlayers = []
    allPlayers =tables[1].find_all('tr')[1:]
    for player in allPlayers:
        redPlayers += [player.find('a', class_ = 'link-blanc').text]
    #............................................................................................................
    
    
scrapeGame('/game/stats/40253/page-game/')