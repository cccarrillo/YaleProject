#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 08:48:09 2021

@author: rdel1cmc
"""

import urllib.request
import json
import math
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#read in the csv file
Lake_data = pd.read_csv("/Users/rdel1cmc/Desktop/rdel1cmc/Desktop/Carra ACE-IT computer/wetlands and coastal/todd/bureau of reclamation/FY21 Info/Yale Project/Habitat_hydrological_data_2021-04-20/Established_Elevation_csv/Saguaro_Lake_elevation_daily.csv")

#start-end point

P1 = [35.44325, -114.65502]
P2 = [35.39065, -114.62344]

#Number of Points
s = 100
interval_lat = (P2[0]-P1[0])/s #interval for latitude
interval_lon = (P2[1]-P1[1])/s #interval for longitude

lat0=P1[0]
lon0=P1[1]

#latitude and longitude list
lat_list=[lat0]
lon_list=[lon0]


#Generating Points
for i in range(s):
    lat_step=lat0+interval_lat
    lon_step=lon0+interval_lon
    lon0=lon_step
    lat0=lat_step
    lat_list.append(lat_step)
    lon_list.append(lon_step)
    
#haversine function
def haversine(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    lon1_rad = math.radians(lon1)
    lon2_rad = math.radians(lon2)
    delta_lat = lat2_rad-lat1_rad
    delta_lon = lon2_rad-lon1_rad
    a=math.sqrt((math.sin(delta_lat/2))**2+math.cos(lat1_rad)*math.cos(lat2_rad)*(math.sin(delta_lon/2))**2)
    d=2*6371000*math.asin(a)
    return d

#distance calculation
d_list = []
for j in range(len(lat_list)):
    lat_p=lat_list[j]
    lon_p=lon_list[j]
    dp=haversine(lat0,lon0,lat_p,lon_p)/1000 #km
    d_list.append(dp)
d_list_rev = d_list[::-1] #reverse list

#construct JSON
d_ar = [{}]*len(lat_list)
for i in range(len(lat_list)):
    d_ar[i] = {"latitude":lat_list[i], "longitude":lon_list[i]}
location = {"locations":d_ar}
json_data = json.dumps(location,skipkeys = int).encode('utf8')

#send request
url = "https://api.open-elevation.com/api/v1/lookup"
response = urllib.request.Request(url,json_data,headers={'Content-Type': 'application/json'})
fp = urllib.request.urlopen(response)

#response processing
res_byte = fp.read()
res_str = res_byte.decode("utf8")
js_str = json.loads(res_str)
#print(js_mystr)
fp.close()

#Getting elevation
response_len = len(js_str['results'])
elev_list = Lake_data['Elevation (ft)']
elev_date = Lake_data['Date']
#for j in range(response_len):
#    elev_list.append(js_str['results'][j]['elevation'])
    
#basic stat information
mean_elev=round((sum(elev_list)/len(elev_list)),3)
min_elev = min(elev_list)
max_elev = max(elev_list)
distance = d_list_rev[-1]




#plot elevation profile
base_reg = 0
plt.figure(figsize=(10,4))
plt.plot(elev_date,elev_list)
plt.plot([0,10000],[min_elev,min_elev],'--g',label='min: '+str(min_elev)+' m')
plt.plot([0,10000],[max_elev,max_elev],'--r',label='max: '+str(max_elev)+' m')
plt.plot([0,10000],[mean_elev,mean_elev],'--y',label='ave: '+str(mean_elev)+' m')
#plt.fill_between(elev_date,elev_list,base_reg,alpha=0.1)
#plt.text(elev_date[0],elev_list[0],"P1")
#plt.text(elev_date[::],elev_list[::],"P2")
plt.xlabel("Date")
plt.ylabel("Elevation(m)")
#plt.grid()
plt.legend(fontsize='small')
plt.show()
