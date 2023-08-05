__version__ = '1.0.5'

import requests
import json
import sys

api_key = "f054a8afdf8d658df832afeccd66c806"

city = sys.argv[1]
state = sys.argv[2]
url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s&appid=%s&units=imperial" % (city, state, api_key)