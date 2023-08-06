#!/usr/bin/env python
import requests
import json
import sys
import weather_in
import datetime
from datetime import datetime
from weather_in import __version__, api_key


def simple(data):
    temp = data['main']['temp']
    low = data['main']['temp_min']
    high = data['main']['temp_max']
    deets = data['weather'][0]['description']
    print(str("the temp is: ")+str(temp))
    print(str("low of: ")+str(low))
    print(str("high of: ")+str(high))
    print(str(deets))

def forecast(data):
    unpack = data['daily']
    dates = []
    count = 0

    for i in unpack:
        while count < 5:
            count = count+1
            dt_text = data['daily'][count]['dt'] #convert
            dt_clean = datetime.utcfromtimestamp(dt_text).strftime('%Y-%m-%d')
            temp_high = data['daily'][count]['temp']['max']
            temp_low = data['daily'][count]['temp']['min']
            wx = data['daily'][count]['weather'][0]['description']
            daily = str(dt_clean)+": high:"+str(temp_high)+", low:"+str(temp_low)+", "+str(wx)
            dates.append(daily)
    print(*dates, sep='\n')

def main():
    city = sys.argv[1]
    state = sys.argv[2]
    country = sys.argv[3] if len(sys.argv) > 3 else 'USA'#1
    query = sys.argv[4] if len(sys.argv) > 4 else 'default'
    geourl = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s,%s&appid=%s&units=imperial" % (city, state, country, api_key) #we always need this url for lat/lon, if using forecasting
    georesp = requests.get(geourl)
    geodata = json.loads(georesp.text)
    lat = geodata['coord']['lat']
    lon = geodata['coord']['lat']
    if query == 'default':
        url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s,%s&appid=%s&units=imperial" % (city, state, country, api_key)
    elif query == '-f' or '--forecast':
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=current,minutely,hourly,alerts&appid=%s&units=imperial" % (lat, lon, api_key)
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if query == 'default':
            simple(data)
        elif query == '-f' or '--forecast':
            forecast(data)

    #except KeyError:
        #print("The API expects City State Country passed as arguments.  Example: Pasadena California USA (note: CA will not work)")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()