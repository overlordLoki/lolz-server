import pandas as pd
from bs4 import BeautifulSoup
import requests


def scrapeGame(link, num_in_tournament,num_of_match,matchName):
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
    gametime = gametime.split(':')
    gametime = int(gametime[0])*60 + int(gametime[1])
    #.............................................................
    #game date
    dateAndWeek = soup.find('div', class_ = 'col-12 col-sm-5 text-right').text.split(' ')
    date = dateAndWeek[0]
    week = dateAndWeek[1]
    #remove first 5 char in week and last char in week
    week = week[5:-1]
    #try make week int
    try:
        week = int(week)
    except:
        week = 0
        week = int(week)
    #................................................................
    #blue team name and win/loss
    blueteambanner  = elem.find('div',class_ ='col-12 blue-line-header').text
    outcome = blueteambanner.split('-')[1]
    blueTeamName = blueteambanner.split('-')[0].replace('\n','')
    blueWin = False
    if(outcome.__contains__('WIN')):
        blueWin = True
    
    #red team name and win/loss
    redteambanner = elem.find('div',class_ ='col-12 red-line-header').text
    outcome = redteambanner.split('-')[1]
    redTeamName = redteambanner.split('-')[0].replace('\n','')
    redWin = False
    if(outcome.__contains__('WIN')):
        redWin = True
    winner = ''
    if(blueWin):
        winner = 'blue'
    elif(redWin):
        winner = 'red'
    #.............................................................
    #game name
    gameName = blueTeamName + " vs " + redTeamName
    #...............................................................
    #region and tourmament
    regionAndTourmament = soup.find('div', class_ = 'col-12 col-sm-7').text.split(' ')
    region,tourmament = tourmAndregion(regionAndTourmament)
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
    blueDragons = blueTeamStats[2].find('span', class_ = 'score-box blue_line').text.split(' ')[0]
    if(blueDragons == ''):
        blueDragons = 0
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
    redDragons = redTeamScores[2].find('span', class_ = 'score-box red_line').text.split(' ')[0]
    if(redDragons == ''):
        redDragons = 0
    #number of barons
    redBarons = redTeamScores[3].find('span', class_ = 'score-box red_line').text
    #number of gold
    redGold = redTeamScores[4].find('span', class_ = 'score-box red_line').text.split('k')[0].split(' ')[1]
    #......................................................................................................
    #table of players and items
    #get tables 'playersInfosLine footable toggle-square-filled'
    tables = soup.find_all('table', class_ = 'playersInfosLine footable toggle-square-filled')
    #get blue team players
    bluePlayers = ''
    allPlayers =tables[0].find_all('a', class_ = 'link-blanc')
    for player in allPlayers:
        bluePlayers += player.text + ','

    #get red team players
    redPlayers = ''
    allPlayers =tables[1].find_all('a', class_ = 'link-blanc')
    for player in allPlayers:
        redPlayers += player.text + ','
        
    #..............................................................................................................
    #totals
    total_kills = int(blueKills) + int(redKills)
    total_towers = int(blueTowers) + int(redTowers)
    total_dragons = int(blueDragons) + int(redDragons)
    total_barons = int(blueBarons) + int(redBarons)
    total_gold = float(blueGold) + float(redGold)
    firstblood_team = ''
    if(blueFB):
        firstblood_team = 'blue'
    elif(redFB):
        firstblood_team = 'red'
    firsttower_team = ''
    if(blueFT):
        firsttower_team = 'blue'
    elif(redFT):
        firsttower_team = 'red'
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
    firsttower_team = ''
    fd_time = 0
    fd_team = ''
    fr_time = 0
    fr_team = ''
    fbaron_time = 0
    fbaron_team = ''
    #if table is not None
    if(table != None):
        #get all rows
        rows = table.find_all('tr')[1:-1]
        fb_time = firstblood(rows)
        ft_time,firsttower_team = towers(rows)
        fd_time, fd_team = Dragons(rows)  
        fr_time, fr_team = riftH(rows)
        fbaron_time, fbaron_team = barons(rows)
    #............................................................................................................
    #make game and return it (to be added to df)
    cols = ['ID', 'Game Name','Match Name','Num in Match','Region', 'Tournament', 'Blue Team Name', 'Red Team Name', 'Date', 'Week', 'Winner', 
            'Blue kills', 'Red kills', 'Total kills', 'Blue towers', 'Red towers', 'Total towers',
            'Blue dragons', 'Red dragons', 'Total dragons', 'Blue barons', 'Red barons', 'Total barons',
            'Blue gold', 'Red gold', 'Total gold', 'First blood team', 'First blood time', 'First tower team',
            'First tower time', 'First dragon team', 'First dragon time', 'First rift herald team', 'First rift herald time',
            'First baron team', 'First baron time', 'Game time','Blue players', 'Red players']    
    GAME = [int(id), gameName,matchName+" "+str(week),int(num_of_match),region, tourmament, blueTeamName, redTeamName, date, week, winner, 
            int(blueKills), int(redKills), int(total_kills) , int(blueTowers), int(redTowers), int(total_towers),
            int(blueDragons) , int(redDragons), int(total_dragons), int(blueBarons), int(redBarons), int(total_barons),
            float(blueGold), float(redGold), float(total_gold),
            firstblood_team, int(fb_time), firsttower_team, int(ft_time), fd_team, int(fd_time), fr_team, int(fr_time), fbaron_team,
            int(fbaron_time),gametime, bluePlayers, redPlayers]
    gamedf = pd.DataFrame([GAME], columns = cols)
    return gamedf

def tourmAndregion(regionAndTourmament):
    region = regionAndTourmament[0][1:5]
    tourmament = region+ " " + regionAndTourmament[1] + ' ' + regionAndTourmament[2]
    if(regionAndTourmament[2] == 'Playoffs'):
        tourmament = tourmament + ' ' + regionAndTourmament[3]
    #remove last element in list
    regionAndTourmament = regionAndTourmament[:-1]
    return region,tourmament

def firstblood(rows):
    #find first blood time
    for row in rows:
        f = row.find_all('td')
        ff = f[4].find('img', src = "../_img/kill-icon.png")
        if(ff != None):
            fb_time = f[0].text
                #fb time to seconds
            fb_time = int(fb_time.split(':')[0]) * 60 + int(fb_time.split(':')[1])
            break
    return fb_time

def towers(rows):
    #find first tower time
    for row in rows:
        f = row.find_all('td')
        ff = f[4].find('img', src = "../_img/tower-icon.png")
        if(ff != None):
            ft_time = f[0].text
            #ft time to seconds
            ft_time = int(ft_time.split(':')[0]) * 60 + int(ft_time.split(':')[1])
            teamflag = f[1].find('img', class_ = "champion_icon_light")
            if(teamflag != None and 'blue' in teamflag.get('src')):
                firsttower_team = 'blue'
            else:
                firsttower_team = 'red'
            break
    return ft_time,firsttower_team

def Dragons(rows):
    #find first dragon time
    for row in rows:
        f = row.find_all('td')
        ff = f[4].find('img', class_ = "champion_icon_light")
        #true if src contains 'dragon'
        if(ff != None and ('dragon' or 'drake' in ff.get('src'))):
            fd_time = f[0].text
            #fd time to seconds
            fd_time = int(fd_time.split(':')[0]) * 60 + int(fd_time.split(':')[1])
            #get team (blue or red)
            teamflag = f[1].find('img', class_ = "champion_icon_light")
            if(teamflag != None and 'blue' in teamflag.get('src')):
                fd_team = 'blue'
            else:
                fd_team = 'red'
            break
    return fd_time,fd_team

def riftH(rows):
    #find first rift herald time
    for row in rows:
        f = row.find_all('td')
        ff = f[4].find('img', src = "../_img/herald-icon.png")
        if(ff != None):
            fr_time = f[0].text
            #fr time to seconds
            fr_time = int(fr_time.split(':')[0]) * 60 + int(fr_time.split(':')[1])
            #get team (blue or red)
            teamflag = f[1].find('img', class_ = "champion_icon_light")
            if(teamflag != None and 'blue' in teamflag.get('src')):
                fr_team = 'blue'
            else:
                fr_team = 'red'
            break
    return fr_time,fr_team

def barons(rows):
    #find first baron time
    for row in rows:
        f = row.find_all('td')
        ff = f[4].find('img', src = "../_img/nashor-icon.png")
        if ff is None:
            fbaron_time = 0
            fbaron_team = 'none'
        else:
            fbaron_time = f[0].text
            #fbaron time to seconds
            fbaron_time = int(fbaron_time.split(':')[0]) * 60 + int(fbaron_time.split(':')[1])
            teamflag = f[1].find('img', class_ = "champion_icon_light")
            fbaron_team = 'blue' if (teamflag != None and 'blue' in teamflag.get('src')) else 'red'
            break
    return fbaron_time,fbaron_team

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
    if (tourmament_name.__contains__('Spring')):
        tNum = 2 if (tourmament_name.__contains__('Playoffs')) else 1
    elif (tourmament_name.__contains__('Summer')):
        tNum = 4 if (tourmament_name.__contains__('Playoffs')) else 3
    elif(tourmament_name.__contains__('MSI')):
        tNum = 5;
    elif(tourmament_name.__contains__('Worlds')):
        tNum = 6;
    #number for the year
    yearNum = tourmament_name.split(' ')[-1][-2:]
    if(yearNum == 'R)'):
        yearNum = tourmament_name.split(' ')[1]
    #build id and return it
    s = str(number_in_tourmament) + str(tNum) + str(regNum) + str(yearNum)
    return int(s)



#for testing purposes
# gametoprint = scrapeGame('/game/stats/35847/page-game/',1,1,'OMG vs TT')
# gametoprint.to_csv('game.csv')