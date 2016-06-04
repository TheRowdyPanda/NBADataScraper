import pandas as pd
import requests
import numpy as np
from datetime import datetime, date
from bs4 import BeautifulSoup
from pyzipcode import ZipCodeDatabase
import json



zcdb = ZipCodeDatabase()



print("start getting weather")


metaData = pd.read_csv("gameMetaData_playoff_2016.csv")

#http://espn.go.com/nba/game?gameId=400827911
#BASE_URL = 'http://espn.go.com/nba/game?gameId={0}'
#print(BASE_URL.format(games['id'][0]))

#key = b587d81757d1943778223b20d9fd77c8
#https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME


#request = requests.get(BASE_URL.format(games['id'][0]))



ids = []
latlons = []
dates = []
times = []
caps = []
atts = []
refs1 = []
refs2 =[]
refs3 = []
temp = []
vis = []
apptemp = []
pressure = []
windspeed = []
cloudcover = []
windbearing = []
precintensity = []
dewpoint = []
precprob = []
dailymintemp = []
dailymaxtemp = []
moonphase = []
maxprecint = []
dailyhum = []




k = 0
print("start for loop")
for index, row in metaData.iterrows():
    #print(metaData['Game ID'][index])
    #print(metaData['Cities'][index])
    cityState = metaData['Cities'][index];
    city = cityState.split(',',1)[0];
    stad = metaData['Stadiums'][index];
    date = metaData['Dates'][index];
    time = metaData['Times'][index];
    time = time[0:len(time)-1];
    string = date + 'T' + time + ':00';
    latLon = 0;
    if city == 'Boston':
	latLon = '42.366303,-71.062228';
    elif city == 'Milwaukee':
	latLon = '43.043611,-87.916944';
    elif city == 'Atlanta':
	latLon = '33.757222,-84.396389';
    elif city == 'Charlotte':
	latLon = '35.225,-80.839167';
    elif city == 'Miami':
	latLon = '25.781389,-80.188056';
    elif city == 'Orlando':
	latLon = '28.539338,-81.383963';
    elif city == 'Washington':
	latLon = '38.898056,-77.020833';
    elif city == 'Denver':
	latLon = '39.748611,-105.0075';
    elif city == 'Minneapolis':
	latLon = '44.979444,-93.276111';
    elif city == 'Portland':
	latLon = '45.531667,-122.666667';
    elif city == 'Oklahoma City':
	latLon = '35.463333,-97.515';
    elif city == 'Brooklyn':
	latLon = '40.682760,-73.975097';
    elif city == 'Salt Lake City':
	latLon = '40.768333,-111.901111';
    elif city == 'Oakland':
	latLon = '37.750278,-122.203056';
    elif city == 'Los Angeles':
	latLon = '34.043056,-118.267222';
    elif city == 'Phoenix':
	latLon = '33.445833,-112.071389';
    elif city == 'Sacramento':
	latLon = '38.649167,-121.518056';
    elif city == 'Dallas':
	latLon = '32.790556,-96.810278';
    elif city == 'Houston':
	latLon = '29.750833,-95.362222';
    elif city == 'Memphis':
	latLon = '35.138333,-90.050556';
    elif city == 'New Orleans':
	latLon = '29.948889,-90.081944';
    elif city == 'New York':
	latLon = '40.750556,-73.993611';
    elif city == 'Newark':
	latLon = '40.733646, -74.171145';
    elif city == 'East Rutherford':
	latLon = '40.811692, -74.067553';
    elif city == 'San Antonio':
	latLon = '29.426944,-98.4375';
    elif city == 'Philadelphia':
	latLon = '39.901111,-75.171944';
    elif city == 'Toronto':
	latLon = '43.643333,-79.379167';
    elif city == 'Chicago':
	latLon = '41.880556,-87.674167';
    elif city == 'Cleveland':
	latLon = '41.496389,-81.688056';
    elif city == 'Detroit':
	latLon = '42.696944,-83.245556';
    elif city == 'Indianapolis':
	latLon = '39.763889,-86.155556';
    elif city == 'Mexico City':
	latLon = '19.498069,-99.175009';
    elif city == 'Seattle':
	latLon = '47.622198, -122.353977'
    else:
	latLon = '1';
    if latLon == '1':
	print(city);
    elif k <= 100:
	k = k;
	retString = latLon + ',' + string;
	print(retString);
	urlString = 'https://api.forecast.io/forecast/b587d81757d1943778223b20d9fd77c8/' + retString;
	#https://api.forecast.io/forecast/APIKEY/LATITUDE,LONGITUDE,TIME
	request = requests.get(urlString);
	#print(request.text);
	dict = json.loads(request.text);
	sum = dict['currently'];

	temper = [];
	if 'temperature' in sum:
		temper = sum['temperature'];

	hum = [];
	if 'humidity' in sum:
		hum = sum['humidity'];

	visi = [];
	if 'visibility' in sum:
		visi = sum['visibility'];

	appTemp = [];
	if 'apparentTemperature' in sum:
		appTemp = sum['apparentTemperature'];

	press = []
	if 'pressure' in sum:
		press = sum['pressure'];

	windSpeed = [];
	if 'windSpeed' in sum:
		windSpeed = sum['windSpeed'];

	cloud = [];
	if 'cloudCover' in sum:
		cloud = sum['cloudCover'];

	windBearing = [];
	if 'windBearing' in sum:
		windBearing = sum['windBearing'];

	precInt = [];
	if 'precipIntensity' in sum:
		precInt = sum['precipIntensity'];

	dewPoint = [];
	if 'dewPoint' in sum:
		dewPoint = sum['dewPoint'];

	precProb = [];
	if 'precipProbability' in sum:
		precProb = sum['precipProbability'];

	sum2 = dict['daily']['data'][0];

	minTemp = [];
	if 'temperatureMin' in sum2:
		minTemp = sum2['temperatureMin'];

	maxTemp = [];
	if 'temperatureMax' in sum2:
		maxTemp = sum2['temperatureMax'];

	moonPhase = [];
	if 'moonPhase' in sum2:
		moonPhase = sum2['moonPhase'];

	precipIntensityMax = [];
	if 'precipIntensityMax' in sum2:
		precipIntensityMax = sum2['precipIntensityMax'];

	dailyHum = [];
	if 'humidity' in sum2:
		dailyHum = sum2['humidity'];
	
	gameID = metaData['Game ID'][index];
	att = metaData['Attendance'][index];
	capac = metaData['Capacities'][index];
	refer1 = metaData['Referee 1'][index];
	refer2 = metaData['Referee 2'][index];
	refer3 = metaData['Referee 3'][index];
	ids.append(gameID)
	latlons.append(latLon)
	dates.append(date)
	times.append(time)
	caps.append(capac)
	atts.append(att)
	refs1.append(refer1)
	refs2.append(refer2)
	refs3.append(refer3)
	temp.append(temper)
	vis.append(visi)
	apptemp.append(appTemp)
	pressure.append(press)
	windspeed.append(windSpeed)
	cloudcover.append(cloud)
	windbearing.append(windBearing)
	precintensity.append(precInt)
	dewpoint.append(dewPoint)
	precprob.append(precProb)
	dailymintemp.append(minTemp)
	dailymaxtemp.append(maxTemp)
	moonphase.append(moonPhase)
	maxprecint.append(precipIntensityMax)
	dailyhum.append(dailyHum)
	print(minTemp);
	
    #if city == 'Mexico City':
    #    latLon = '19.498069, -99.175009';
    #else:
#	print('none');
 #   		#numZips = zcdb.find_zip(city=city);
		##zip = numZips[0];
		#latLon = str(zip.longitude) + ',' + str(zip.latitude);
    #print(loc)
    #print(arena)
    #print(date)
    #print(time)
    #print(stadiumSize)
    #print(attendance)
    #print(refs)



#print(len(gameIds))
dic = {'ids':ids, 'latLon':latlons, 'date':dates, 'time':times, 'attendance':atts, 'capacity':caps, 'Referee 1':refs1, 'Referee 2':refs2, 'Referee 3':refs3, 'temperature':temp, 'visibility':vis, 'appTemp':apptemp, 'pressure':pressure, 'wind speed':windspeed, 'cloud cover':cloudcover, 'wind bearing':windbearing, 'precipitation intensity':precintensity, 'dew point':dewpoint, 'precipitation probability':precprob, 'daily min temp':dailymintemp, 'daily max temp':dailymaxtemp, 'moon phase':moonphase, 'daily humidity':dailyhum}

#dic = {'Game ID': gameIds, 'Cities': cities, 'Stadiums':stadiums, 'Dates':dates, 'Times': times, 'Capacities':caps, 'Attendance':atts, 'Referee 1': refs1, 'Referee 2':refs2, 'Referee 3':refs3}

finalList = pd.DataFrame(dic, index=ids)
#teams.index.name = 'team'
#print(teams)
finalList.to_csv("gameMetaData_playoff_final_2016.csv")


