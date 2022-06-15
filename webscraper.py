import pandas as pd
from bs4 import BeautifulSoup
import requests
import scrapGame


    
def scrapeTourn(url):
    #link to the page
    source = requests.get(url , headers = {'User-agent': 'your bot 0.1'}).text
    #souping the page
    soup = BeautifulSoup(source, 'lxml')
    #make a list of all the match links
    links = []
    for m in soup.find_all('td', class_ = 'text-left'):
        #add the href of the link to the list
        links.append(m.find('a').get('href'))
    #remove the first 2 char in each link
    for i in range(len(links)):
        links[i] = links[i][2:]
    #reverse the list so the most recent game is first
    links = links[::-1]
    #number of games currently in the tournament
    num_in_tourn = 1
    #dataframe to store the games
    # id, game name, tourmament , blue team name, red team name, date, week, winner, blue kills, red kills, total kills, blue towers, red towers, total towers,
    # blue dragons, red dragons, total dragons, blue barons, red barons, total barons, blue gold, red gold, total gold,
    # first blood team, first blood time, first tower team, first tower time, first dragon team, first dragon time, first rift herald team, first rift herald time,
    # first baron team , first baron time ,blue players, red players, game time.
    cols = ['ID', 'Game Name', 'Tournament', 'Blue Team Name', 'Red Team Name', 'Date', 'Week', 'Winner', 
            'Blue kills', 'Red kills', 'Total kills', 'Blue towers', 'Red towers', 'Total towers',
            'Blue dragons', 'Red dragons', 'Total dragons', 'Blue barons', 'Red barons', 'Total barons',
            'Blue gold', 'Red gold', 'Total gold', 'First blood team', 'First blood time', 'First tower team',
            'First tower time', 'First dragon team', 'First dragon time', 'First rift herald team', 'First rift herald time',
            'First baron team', 'First baron time', 'Game time','Blue players', 'Red players']
    #create the dataframe
    df = pd.DataFrame(columns = cols)
    #for each link in the list, scrape the page building a match
    for link in links:
        URL = "https://gol.gg"+link;
        source = requests.get(URL, headers = {'User-agent': 'your bot 0.1'}).text
        soup = BeautifulSoup(source, 'lxml')
        #find nav class "class="navbar navbar-expand-md navbar-dark gamemenu""
        menu = soup.find('nav', class_ = 'navbar navbar-expand-md navbar-dark gamemenu').find_all('a')[1:-1]
        gamelinks = []
        #remove first 2 char in each link and add to gamelinks
        for m in menu:
            m = m.get('href')
            m = m[2:]
            gamelinks.append(m)
        
        for game_link in gamelinks:
            game = scrapGame.scrapeGame(game_link,num_in_tourn)
            num_in_tourn += 1
            df = pd.concat([df,game], ignore_index=True)
    return df
    

lec_df = scrapeTourn('https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%20Playoffs%202022/')
lec_df.to_csv('lec_PlayerOffs_2022.csv')