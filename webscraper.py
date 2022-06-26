import pandas as pd
from bs4 import BeautifulSoup
import requests
import scrapGame
    
def scrapeTourn(url):  # sourcery skip: for-append-to-extend, list-comprehension
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
    # id, game name, tourmament , blue team name, red team name, date, week, winner, blue kills, red kills, total kills, blue towers, red towers, total towers,
    # blue dragons, red dragons, total dragons, blue barons, red barons, total barons, blue gold, red gold, total gold,
    # first blood team, first blood time, first tower team, first tower time, first dragon team, first dragon time, first rift herald team, first rift herald time,
    # first baron team , first baron time ,blue players, red players, game time.
    cols = ['ID', 'Game_Name','Match_Name','Num_in_Match','Region', 'Tournament', 'Blue_Team_Name', 'Red_Team_Name', 'Date', 'Week', 'Winner', 
            'Blue_kills', 'Red_kills', 'Total_kills', 'Blue_towers', 'Red_towers', 'Total_towers',
            'Blue_dragons', 'Red_dragons', 'Total_dragons', 'Blue_barons', 'Red_barons', 'Total_barons',
            'Blue_gold', 'Red_gold', 'Total_gold', 'First_blood_team', 'First_blood_time', 'First_tower_team',
            'First_tower_time', 'First_dragon_team', 'First_dragon_time', 'First_rift_herald_team', 'First_rift_herald_time',
            'First_baron_team', 'First_baron_time', 'Game_time','Blue_players', 'Red_players']    
    #create the dataframe
    df = pd.DataFrame(columns = cols)
    df = scrapMatchs(links, num_in_tourn, df)
    return df

def scrapMatchs(links, num_in_tourn, df):
    #for each link in the list, scrape the page building a match
    for link in links:
        URL = "https://gol.gg"+link;
        source = requests.get(URL, headers = {'User-agent': 'your bot 0.1'}).text
        soup = BeautifulSoup(source, 'lxml')
        #get the Match Name
        matchName = soup.find('div', class_='col-12 mt-4').find('h1').text
        #find nav class "class="navbar navbar-expand-md navbar-dark gamemenu""
        menu = soup.find('nav', class_ = 'navbar navbar-expand-md navbar-dark gamemenu').find_all('a')[1:-1]
        gamelinks = []
        #remove first 2 char in each link and add to gamelinks
        for m in menu:
            m = m.get('href')
            m = m[2:]
            gamelinks.append(m)
        #for each game in the match
        num_of_match = 1
        for game_link in gamelinks:
            game = scrapGame.scrapeGame(game_link,num_in_tourn,num_of_match,matchName)
            num_in_tourn += 1
            df = pd.concat([df,game], ignore_index=True)
            num_of_match += 1
    return df
    

#df_to_write = scrapeTourn('https://gol.gg/tournament/tournament-matchlist/MSI%202022/')
#df_to_write.to_csv(df_to_write.iloc[0]['Tournament']+'.csv')