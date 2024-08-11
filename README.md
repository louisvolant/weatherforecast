# weather
Get weather from OpenWeatherMap

## Requirements

1. First install the required packages

Python3, logging, argparse, requests, datetime

````
python3 -m venv myenv
source myenv/bin/activate // on MacOS
source myenv/Scripts/activate // on Windows
pip install requests
````

2. Api Key

You also need to have a API key working from OpenWeatherMap.org

To verify if the API Key is activated : https://api.openweathermap.org/data/2.5/weather?q=paris&appid=GEOLOC_API

Once you have it, create a file config.py and put inside your API Key : 
># config.py
>GEOLOC_API = "dddddddsdfsdfsdfsdfsdzerzer"



## How to execute

Go in the same folder than the python script

````
$ python3 weather.py 'paris' 
````

