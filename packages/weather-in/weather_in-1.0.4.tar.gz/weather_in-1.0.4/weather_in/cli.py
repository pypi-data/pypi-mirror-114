#!/usr/bin/env python

import weather_in
from weather_in import __version__, city, state, api

def main():
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        temp = data['main']['temp']
        low = data['main']['temp_min']
        high = data['main']['temp_max']
        deets = data['weather'][0]['description']
        print(str("the temp is: ")+str(temp))
        print(str("low of: ")+str(low))
        print(str("high of: ")+str(high))
        print(str(deets))
    except KeyError:
        print("The API expects City State passed as arguments.  Example: Pasadena California (note: CA will not work)")
    except:
        print("Whoops, I'm not sure what happened here.  Good luck!")
if __name__ == '__main__':
    main()