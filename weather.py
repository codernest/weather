import json
import os
import sys
import urllib.request
import urllib.parse
from geopy.geocoders import Nominatim

def truncate(n, decimals=0):
    multiplier = 10 ** decimals
    return int(n * multiplier) / multiplier

def realround(n):
    return truncate(n+0.5)

def getweather(address):
    geolocator = Nominatim(user_agent='weather-app')
    location = geolocator.geocode(address)

    owmApiKey = os.getenv('OWM_API_KEY')
    url = 'https://api.openweathermap.org/data/2.5/onecall?lat='+str(location.latitude)+'&lon='+str(location.longitude)+'&exclude=minutely&appid='+owmApiKey
    f = urllib.request.urlopen(url)
    data = f.read()
    encoding = f.info().get_content_charset('utf-8')
    JSON_object = json.loads(data.decode(encoding))

    #print(JSON_object['current'])
    temp = int(realround((JSON_object['current']['temp'] - 273.15) * 9/5 + 32))
    return {
        'location': {
            'address': location.address,
            'latlog': {
                'lat': location.latitude,
                'long': location.longitude
            }
        },
        'description': JSON_object['current']['weather'][0]['description'], 
        'temp': temp
    }

address = sys.argv[1]
weather = getweather(address)
print('location:    '+weather['location']['address'])
print('description: '+weather['description'])
print('temp:        '+str(weather['temp']))
