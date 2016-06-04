import pandas as pd
import requests
import numpy as np
from datetime import datetime, date
from bs4 import BeautifulSoup





print("start getting meta data")


games = pd.read_csv("savedGames_playoffs.csv")
#games = pd.read_csv("savedGames.csv")

#http://espn.go.com/nba/game?gameId=400827911
BASE_URL = 'http://espn.go.com/nba/game?gameId={0}'
print(BASE_URL.format(games['id'][0]))

#request = requests.get(BASE_URL.format(games['id'][0]))

#table = BeautifulSoup(request.text).find('table', class_='mod-data')
#heads = table.find_all('thead')
#print(heads[0].find_all('tr')[0].find_all('th')[1:])
#headers = heads[0].find_all('tr')[0].find_all('th')[1:]
#headers = [th.text for th in headers]
columns = ['id', 'location', 'arena', 'date', 'time', 'stadiumSize', 'attendance', 'refs'] 

#metaData = pd.DataFrame(columns=columns)
#metaData = pd.DataFrame()
metaData = []

gameIds = []
cities = []
stadiums = []
dates = []
times = []
caps = []
atts = []
refs1 = []
refs2 =[]
refs3 = []


print("start for loop")
#games = games[0:8]
for index, row in games.iterrows():
    print(games['id'][index])
    request = requests.get(BASE_URL.format(games['id'][index]))
    table = []
    if len(BeautifulSoup(request.text, "lxml").find_all('div', id='gamepackage-game-information')) > 0:
         table = BeautifulSoup(request.text, "lxml").find_all('div', id='gamepackage-game-information')[0]
    else:
        gameIds.append(games['id'][index])
        cities.append('none')
        stadiums.append('none')
        dates.append('none')
        times.append('none')
        caps.append('none')
        atts.append('none')
        refs1.append('none')
        refs2.append('none')
        refs3.append('none')
        print("poop")
        continue
    #table = BeautifulSoup(request.text, "lxml").find_all('div', id='gamepackage-game-information')[0]
    loc = "none"
    if table.find('div', class_="location-details").li:
        loc = table.find('div', class_="location-details").li.text
    if table.find('div', class_="caption-wrapper"):
        arena = table.find('div', class_="caption-wrapper").text
    else:
        arena = "none"
    dateTime = table.find('div', class_="game-date-time")
    date = dateTime('span')[0]['data-date'].split("T")[0]
    time = dateTime('span')[0]['data-date'].split("T")[1]
    #stadiumSize = table.find_all('div', class_="game-info-note capacity")[1].text
    if len(table.find_all('div', class_="game-info-note capacity")) > 1:
        stadiumSize = table.find_all('div', class_="game-info-note capacity")[1].text
        attendance = table.find_all('div', class_="game-info-note capacity")[0].text
    else:
        stadiumSize = "none"
        attendance = "none"
    #attendance = table.find_all('div', class_="game-info-note capacity")[0].text
    if len(table.find_all('div', class_="game-info-note")) > 2:
        refs = table.find_all('div', class_="game-info-note")[2].text
    else:
        refs = "none"
    #print(loc)
    #print(arena)
    #print(date)
    #print(time)
    #print(stadiumSize)
    #print(attendance)
    #print(refs)
    gameIds.append(games['id'][index])
    cities.append(loc.replace('\t', '').replace('\n', ''))
    stadiums.append(arena.replace('\t', '').replace('\n', ''))
    dates.append(date)
    times.append(time)
    caps.append(stadiumSize)
    atts.append(attendance)
    print(refs)
    if refs is "none":
         refs1.append('none')
         refs2.append('none')
         refs3.append('none')
         continue
    refs = refs.split(':')[1]
    refs = refs.split(',')
    numRefs = len(refs)
    if numRefs == 0:
         refs1.append('none')
         refs2.append('none')
         refs3.append('none')
    if numRefs == 1:
         refs1.append(refs[0].replace(" ",""))
         refs2.append('none')
         refs3.append('none')
    if numRefs == 2:
         refs1.append(refs[0])
         refs2.append(refs[1])
         refs3.append('none')
    if numRefs == 3:
         refs1.append(refs[0])
         refs2.append(refs[1])
         refs3.append(refs[2])
    #gameIds.append(games['id'][index])
    numPuts = 7
    #loadData = [games['id'][index], loc.replace('\t', '').replace('\n', ''), arena.replace('\t', '').replace('\n', ''), date, time, stadiumSize, attendance, refs]
    #print(loadData)
    #loadData = loadData.reshape(1, len(loadData)
    #array = np.zeros((1, numPuts + 1), dtype=object)
    #frame = pd.DataFrame(columns=columns)
    #print(frame)
    #for x in loadData:
        #line = np.concatenate((games['id'][index], x)).reshape(1,len(columns))
        #new = pd.DataFrame(line, columns=frame.columns)
        #frame.append(x)
    #metaData = metaData.append(loadData, ignore_index=True)
    #metaData.append(loadData)


#print(len(gameIds))
print(cities)
print(refs1)
print(refs3)

dic = {'Game ID': gameIds, 'Cities': cities, 'Stadiums':stadiums, 'Dates':dates, 'Times': times, 'Capacities':caps, 'Attendance':atts, 'Referee 1': refs1, 'Referee 2':refs2, 'Referee 3':refs3}

finalList = pd.DataFrame(dic, index=gameIds)
#teams.index.name = 'team'
#print(teams)
finalList.to_csv("gameMetaData_playoff_2016.csv")

    
#players = players.set_index('id')
#players = players.encode('ascii', encoding='utf-8')
#print(metaData)
#metaData.to_csv('metadata.csv', encoding='utf-8')
#copper.save(players, 'players')


