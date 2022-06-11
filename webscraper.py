# Adding libraries needed
from re import M
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests



 
#link to the page
source = requests.get('https://gol.gg/tournament/tournament-matchlist/LEC%20Spring%20Playoffs%202022/' , headers = {'User-agent': 'your bot 0.1'}).text
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
#for each link in the list, scrape the page
for link in links:
    URL = "https://gol.gg"+link;
    source = requests.get(URL, headers = {'User-agent': 'your bot 0.1'}).text
    soup = BeautifulSoup(source, 'lxml')
    #find nav class "class="navbar navbar-expand-md navbar-dark gamemenu""
    games_links_class = soup.find('nav', class_ = 'navbar navbar-expand-md navbar-dark gamemenu')
    games_links = []
    for i in games_links_class.find_all('a')[1:-1]:
        #add the href of the link to the list
        games_links.append(i.get('href'))
    
    
    
