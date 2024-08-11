# weather.py

import requests
import logging
import argparse
from datetime import datetime
from config import GEOLOC_API

GEOCODING_API = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_API_V3 = "https://api.openweathermap.org/data/3.0/onecall"
WEATHER_API_V2 = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_API_V2 = "http://api.openweathermap.org/data/2.5/forecast"

# README
# execute with
# python3 -m venv myenv
# source myenv/bin/activate # on MacOS
# source myenv/Scripts/activate # on Windows
# pip install requests
# python3 weather.py 'paris' 
# To verify if the API Key is activated : https://api.openweathermap.org/data/2.5/weather?q=paris&appid=GEOLOC_API
# Once finished, simply desactivate the virtual environment using "deactivate"

def get_city_location(api_key, city):
    base_url = GEOCODING_API

    params = {
        'q': city,
        'appid': api_key,
        'limit': '3',       # Quantity of cities to list
        'lang': 'fr'        # Pour obtenir les descriptions en français
    }

    response = requests.get(base_url, params=params)

    #logging.info('City Location Response: {0}'.format(response))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None
    
def print_location(data):
    if data:
        firstresult = data[0]
        
        print(f"Localization pour {firstresult['name']}, {firstresult['country']}:")
        print(f"Latitude: {firstresult['lat']}")
        print(f"Longitude: {firstresult['lon']}")
        if('state' in firstresult):
            print(f"Région: {firstresult['state']}")
    else:
        print("Erreur : impossible de récupérer les données de localization")

def get_weather_v2(api_key, city):
    base_url = WEATHER_API_V2
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',  # Pour obtenir les températures en Celsius
        'lang': 'fr'        # Pour obtenir les descriptions en français
    }
    
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def print_weather(data):
    if data:
        print(f"Météo pour {data['name']}, {data['sys']['country']}:")
        print(f"Description: {data['weather'][0]['description']}")
        print(f"Température: {data['main']['temp']}°C")
        print(f"Température ressentie: {data['main']['feels_like']}°C")
        print(f"Humidité: {data['main']['humidity']}%")
        print(f"Vitesse du vent: {data['wind']['speed']} m/s")
    else:
        print("Erreur : impossible de récupérer les données météorologiques")

def get_forecast_v2(api_key, lat, lon):
    base_url = FORECAST_API_V2
    params = {
        'lat': lat,
        'lon': lon,
        'appid': api_key,
        'units': 'metric',  # Pour obtenir les températures en Celsius
        'lang': 'fr'        # Pour obtenir les descriptions en français
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None

def print_forecast(data):
    if data:
        if data['list']:
            listing = data['list']
            for elt in listing:
                print(f"Météo pour {datetime.fromtimestamp(elt['dt'])}." +
                      f"\tTempérature : {elt['main']['temp']}°C " +
                      f"\t\tRessentie : {elt['main']['feels_like']}°C" +
                      f"\tMini : {elt['main']['temp_min']}°C" +
                      f"\tMaxi : {elt['main']['temp_max']}°C"+
                      f"\tType : {elt['weather'][0]['description']}" + 
                      "")
    else:
        print("Erreur : impossible de récupérer les données météorologiques")


def main():
    parser = argparse.ArgumentParser(description='Retrieve weather for a given city.')
    parser.add_argument('city', type=str, help='The city you wish to request weather for')
    args = parser.parse_args()


    logging.info('Calling Localization for: {0} with api key {1}'.format(args.city, GEOLOC_API))
    city_location = get_city_location(GEOLOC_API, args.city)
    print_location(city_location)

    logging.info('Calling weather for: {0} with api key {1}'.format(args.city, GEOLOC_API))
    weather_data = get_weather_v2(GEOLOC_API, args.city)
    print_weather(weather_data)

    if city_location:
        firstresult = city_location[0]
        logging.info('Calling Forecast for: {0}/{1} with api key {2}'.format(firstresult['lat'],firstresult['lon'], GEOLOC_API))
        forecast_data = get_forecast_v2(GEOLOC_API, firstresult['lat'], firstresult['lon'])
        print_forecast(forecast_data)
    else:
        logging.info('Not calling Forecast because no City Location')



if __name__ == '__main__':
    ## Initialize logging before hitting main, in case we need extra debuggability
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    main()
