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
    #blue team stats
    blueScores = elem.find_all('span', class_ = 'score-box blue_line')
    blueKills = blueScores[0].text
    print(blueKills)
    
scrapeGame('/game/stats/40253/page-game/')