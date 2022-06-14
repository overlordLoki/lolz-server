from re import I, T
from bs4 import BeautifulSoup
import requests

def idMaker(tourmament_name, number_in_tourmament):
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
    if(tourmament_name.__contains__('Spring')):
        tNum = 1;
        if(tourmament_name.__contains__('Playoffs')):
            tNum = 2;
    elif(tourmament_name.__contains__('Summer')):
        tNum = 3;
        if(tourmament_name.__contains__('Playoffs')):
            tNum = 4;
    elif(tourmament_name.__contains__('MSI')):
        tNum = 5;
    elif(tourmament_name.__contains__('Worlds')):
        tNum = 6;
    #number for the year
    yearNum = tourmament_name.split(' ')[-1][-2:]
    #build id and return it
    s = str(number_in_tourmament) + str(tNum) + str(regNum) + str(yearNum)
    id = int(s)
    return id

def scrapeGame(link, num_in_tournament):
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
    if(isinstance(week, int)):
        week = int(week)
    else:
        week = 0
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
    if(regionAndTourmament[2] == 'Playoffs'):
        tourmament = tourmament + ' ' + regionAndTourmament[3]
    #remove last element in list
    regionAndTourmament = regionAndTourmament[:-1]
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
    allPlayers =tables[0].find_all('a', class_ = 'link-blanc')
    for player in allPlayers:
        bluePlayers += [player.text]

    #get red team players
    redPlayers = []
    allPlayers =tables[1].find_all('a', class_ = 'link-blanc')
    for player in allPlayers:
        redPlayers += player.text
    #............................................................................................................
    #game id
    id = idMaker(tourmament,num_in_tournament)
    #events........................................................................................................
    url = URL[:-5] + 'timeline/'
    source2 = requests.get(url, headers = {'User-agent': 'your bot 0.1'}).text
    soup2 = BeautifulSoup(source2, 'lxml')
    #get table of events
    table = soup2.find('table' , class_ = 'nostyle timeline trhover')
    #firstblood time ,first tower time, first dragon time and first rift herald time
    fb_time = 0
    ft_time = 0
    fd_time = 0
    fd_team = ''
    fr_time = 0
    fr_team = ''
    fbr_time = 0
    fbr_team = ''
    #if table is not None
    if(table != None):
        #get all rows
        rows = table.find_all('tr')[1:-1]
        #find first blood time
        for row in rows:
            f = row.find_all('td')
            ff = f[4].find('img', src = "../_img/kill-icon.png")
            if(ff != None):
                fb_time = f[0].text
                break
        #find first tower time
        for row in rows:
            f = row.find_all('td')
            ff = f[4].find('img', src = "../_img/tower-icon.png")
            if(ff != None):
                ft_time = f[0].text
                break
        #find first dragon time
        for row in rows:
            f = row.find_all('td')
            ff = f[4].find('img', class_ = "champion_icon_light")
            #print true if src contains 'dragon'
            if(ff != None and 'dragon' in ff.get('src')):
                fd_time = f[0].text
                #get team (blue or red)
                teamflag = f[1].find('img', class_ = "champion_icon_light")
                if(teamflag != None and 'blue' in teamflag.get('src')):
                    fd_team = blue
                else:
                    fd_team = red
                break  
        #find first rift herald time
        for row in rows:
            f = row.find_all('td')
            ff = f[4].find('img', src = "../_img/herald-icon.png")
            if(ff != None):
                fr_time = f[0].text
                #get team (blue or red)
                teamflag = f[1].find('img', class_ = "champion_icon_light")
                if(teamflag != None and 'blue' in teamflag.get('src')):
                    fr_team = blue
                else:
                    fr_team = red
                break
        #find first baron time
        for row in rows:
            f = row.find_all('td')
            ff = f[4].find('img', src = "../_img/baron-icon.png")
            if(ff != None):
                fbr_time = f[0].text
                teamflag = f[1].find('img', class_ = "champion_icon_light")
                if(teamflag != None and 'blue' in teamflag.get('src')):
                    fbr_team = blue
                else:
                    fbr_team = red
    #............................................................................................................
    #make game [] and return it (to be added to df)
    GAME = [id,tourmament,num_in_tournament,blueTeam,redTeam,blueKills,redKills,blueTowers,
            redTowers,blueDragons,redDragons,blueBarons,redBarons,blueGold,redGold,blueFB,redFB,
            fb_time,ft_time,fd_time,fd_team,fr_time,fr_team,fbr_time,fbr_team,bluePlayers,redPlayers]
    return GAME



#scrapeGame('/game/stats/40253/page-game/',1)
scrapeGame('/game/stats/39726/page-game/',1)