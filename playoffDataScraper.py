import pandas as pd
import requests
import numpy as np
from datetime import datetime, date
from bs4 import BeautifulSoup

url = 'http://espn.go.com/nba/teams'
r = requests.get(url)

soup = BeautifulSoup(r.text)
tables = soup.find_all('ul', class_='medium-logos')

teams = []
prefix_1 = []
prefix_2 = []
teams_urls = []
for table in tables:
    lis = table.find_all('li')
    for li in lis:
        info = li.h5.a
        teams.append(info.text)
        url = info['href']
        teams_urls.append(url)
        prefix_1.append(url.split('/')[-2])
        prefix_2.append(url.split('/')[-1])


dic = {'url': teams_urls, 'prefix_2': prefix_2, 'prefix_1': prefix_1}
teams = pd.DataFrame(dic, index=teams)
teams.index.name = 'team'
#print(teams)
teams.to_csv("saveTeams.csv")















year = 2016
#BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/{2}'
BASE_URL = 'http://espn.go.com/nba/team/schedule/_/name/{0}/year/{1}/seasontype/3/{2}'

match_id = []
dates = []
home_team = []
home_team_score = []
visit_team = []
visit_team_score = []
teams = pd.read_csv("saveTeams.csv")

for index, row in teams.iterrows():
    _team, url = row['team'], row['url']
    print(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
    r = requests.get(BASE_URL.format(row['prefix_1'], year, row['prefix_2']))
    if r.text.find('Postseason') == -1:
	continue
    table = BeautifulSoup(r.text).table
    if not table:
    	continue
    for row in table.find_all('tr')[1:]: # Remove header
        columns = row.find_all('td')
        try:
            _home = True if columns[1].li.text == 'vs' else False
            _other_team = columns[1].find_all('a')[1].text
            _score = columns[2].a.text.split(' ')[0].split('-')
            _won = True if columns[2].span.text == 'W' else False

            match_id.append(columns[2].a['href'].split('?id=')[1])
            home_team.append(_team if _home else _other_team)
            visit_team.append(_team if not _home else _other_team)
            d = datetime.strptime(columns[0].text, '%a, %b %d')
            dates.append(date(year, d.month, d.day))

            if _home:
                if _won:
                    home_team_score.append(_score[0])
                    visit_team_score.append(_score[1])
                else:
                    home_team_score.append(_score[1])
                    visit_team_score.append(_score[0])
            else:
                if _won:
                    home_team_score.append(_score[1])
                    visit_team_score.append(_score[0])
                else:
                    home_team_score.append(_score[0])
                    visit_team_score.append(_score[1])
        except Exception as e:
            pass # Not all columns row are a match, is OK
            # print(e)



numGames = len(dates)
match_id = match_id[0:numGames]
home_team = home_team[0:numGames]
visit_team = visit_team[0:numGames]
home_team_score = home_team_score[0:numGames]
visit_team_score = visit_team_score[0:numGames]

print(len(match_id))
print(len(dates))
print(len(home_team))
print(len(visit_team))
print(len(home_team_score))
print(len(visit_team_score))

dic = {'id': match_id, 'date': dates, 'home_team': home_team, 'visit_team': visit_team,
        'home_team_score': home_team_score, 'visit_team_score': visit_team_score}



games = pd.DataFrame(dic).drop_duplicates(subset='id').set_index('id')
#print(games)

games.to_csv('savedGames_playoffs.csv')



print("DID SAVE GAMES")
print("DID SAVE GAMES")











print("start getting player data")


games = pd.read_csv("savedGames_playoffs.csv")

BASE_URL = 'http://espn.go.com/nba/boxscore?gameId={0}'
print(BASE_URL.format(games['id'][0]))

request = requests.get(BASE_URL.format(games['id'][0]))

table = BeautifulSoup(request.text).find('table', class_='mod-data')
heads = table.find_all('thead')
#print(heads[0].find_all('tr')[0].find_all('th')[1:])
headers = heads[0].find_all('tr')[0].find_all('th')[1:]
headers = [th.text for th in headers]
columns = ['id', 'team', 'player', 'position'] + headers

players = pd.DataFrame(columns=columns)

def get_players(players, team_name, game_id):
    array = np.zeros((len(players), len(headers)+2), dtype=object)
    array[:] = np.nan
    for i, player in enumerate(players):
        cols = player.find_all('td')
	lastLets = cols[0].text.split(',')[0][-2:]
	sLen = len(cols[0].text.split(',')[0])
	if lastLets.isupper() == True:
		array[i, 0] = cols[0].text.split(',')[0][:sLen - 2]
		array[i, 1] = cols[0].text.split(',')[0][-2:]
	else:
		array[i, 0] = cols[0].text.split(',')[0][:sLen - 1]
		array[i, 1] = cols[0].text.split(',')[0][-1:]
        #array[i, 0] = cols[0].text.split(',')[0]
        #array[i, 1] = "DAMN"
	print(cols[0].text.split(',')[0])
        for j in range(2, len(headers) + 2):
            if not cols[1].text.startswith('DNP'):
		if not cols[1].text.startswith('Did not play'):
			print(cols[j-1].text)
                	array[i, j] = cols[j-1].text

    frame = pd.DataFrame(columns=columns)
    for x in array:
        line = np.concatenate(([game_id, team_name], x)).reshape(1,len(columns))
        new = pd.DataFrame(line, columns=frame.columns)
        frame = frame.append(new)
    return frame

print("start for loop")
#games = games[0:2]
for index, row in games.iterrows():
    print(games['id'][index])
    request = requests.get(BASE_URL.format(games['id'][index]))
    table = BeautifulSoup(request.text, "lxml").find_all('table', class_='mod-data')
    print("START TABLE")
    print(table)
    print("END TABLE")
    if not table:
        continue
    table1 = table[0]
    table2 = table[1]
    #print(table)
    #print(BeautifulSoup(request.text))
    heads1 = table1.find_all('thead')
    heads2 = table2.find_all('thead')
    bodies1 = table1.find_all('tbody')
    bodies2 = table2.find_all('tbody')
    teamDivs = BeautifulSoup(request.text, "lxml").find_all('div', class_='table-caption')
    team1Div = teamDivs[0]
    team2Div = teamDivs[1]

    #team_1 = heads1[0].th.text
    team_1 = [s for s in team1Div.children if isinstance(s, basestring)][0]
    team_1_players = bodies1[0].find_all('tr') + bodies1[1].find_all('tr')
    team_1_players = get_players(team_1_players, team_1, games['id'][index])
    players = players.append(team_1_players)

    #team_2 = heads2[0].th.text
    team_2 = [s for s in team2Div.children if isinstance(s, basestring)][0]
    team_2_players = bodies2[0].find_all('tr') + bodies2[1].find_all('tr')
    team_2_players = get_players(team_2_players, team_2, games['id'][index])
    players = players.append(team_2_players)

players = players.set_index('id')
#players = players.encode('ascii', encoding='utf-8')
print(players)
players.to_csv('savedPlayerDataPlayoff_holder.csv', encoding='utf-8')



