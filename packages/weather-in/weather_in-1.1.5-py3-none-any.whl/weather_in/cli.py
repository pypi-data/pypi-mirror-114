#!/usr/bin/env python
import requests
import json
import sys
import weather_in
import datetime
from datetime import datetime
from weather_in import __version__, api_key
import argparse

parser = argparse.ArgumentParser(description='A simple OpenWeather API wrapper.')
parser.add_argument('city', type=str)
parser.add_argument('state', type=str)
parser.add_argument('country', type=str, nargs='*')
parser.add_argument("-f", "--forecast", required=False,
   help="Five-day forecast.", nargs='*')

args = vars(parser.parse_args())


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
    city = args['city']
    state = args['state']
    country = args['country'] if args['country'] is not None else 'USA' #1
    geourl = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s,%s&appid=%s&units=imperial" % (city, state, country, api_key) #we always need this url for lat/lon, if using forecasting
    georesp = requests.get(geourl)
    geodata = json.loads(georesp.text)
    lat = geodata['coord']['lat']
    lon = geodata['coord']['lat']
    if args['forecast'] is None:
        url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s,%s&appid=%s&units=imperial" % (city, state, country, api_key)
    elif args['forecast'] is not None:
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&exclude=current,minutely,hourly,alerts&appid=%s&units=imperial" % (lat, lon, api_key)
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if args['forecast'] is None:
            simple(data)
        elif args['forecast'] is not None:
            forecast(data)

    #except KeyError:
        #print("The API expects City State Country passed as arguments.  Example: Pasadena California USA (note: CA will not work)")
    except Exception as e:
        print(e)
if __name__ == '__main__':
    main()