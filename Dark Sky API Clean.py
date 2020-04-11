# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 17:19:03 2019

@author: michael.gutierrez
"""

import forecastio
import datetime
import pandas as pd 

#input api key
api_key = ''

#list of lat long coordinates
stores1 = pd.read_csv("")

#define start date for api data pull
start = datetime.datetime(2018, 5, 6)
    
#Function for pulling data from darksky api
def percip (lat2, lng2):
    lat2 = lat2
    lng2 = lng2
    #define whihc attributes to pull from darksky api go to https://darksky.net/dev/docs for more info
    attributes = ["uvIndex", "icon","temperatureLow", "precipIntensity", "precipProbability","cloudCover","humidity","temperatureHigh","windGust","windSpeed","visibility","sunriseTime","sunsetTime","summary"]
    times = []
    data = {}
    #will loop over each attribute defined above
    for attr in attributes:
        data[attr] = []    
    #define range of dates to be pulled    
    for offset in range(41, 50):
        #load in data from api
        forecast = forecastio.load_forecast(api_key, lat2, lng2, time=start+datetime.timedelta(offset), units="us")
       #pulls data at daily level
        da = forecast.daily()
        d = da.data
        #builds out data frame for each time/attribute
        for p in d:
            times.append(p.time)
            for attr in attributes:
                data[attr].append(p.d[attr])
    df2 = pd.DataFrame(data, index=times)
    #labels each df with correct lat long coordinates
    df2['lat'] = lat2
    df2['lng'] = lng2
    return (df2);

#for loop to run api call funciton against df of lat longs
df3 = pd.DataFrame(columns = ["uvIndex", "icon","temperatureLow","PercipType","precipIntensity", "precipProbability","cloudCover","humidity","temperatureHigh","windGust","windSpeed","visibility","sunriseTime","sunsetTime","summary"])
for index, row in stores1.iterrows():
    df2 = percip(row['latitude'],row['longitude'])
    df3 = df3.append(df2)

#write to csv
df3.to_csv(".csv",index = True)



