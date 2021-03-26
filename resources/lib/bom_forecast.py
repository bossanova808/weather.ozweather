import requests
import re
from bs4 import BeautifulSoup
from common import *

"""
Kodi Weather Info Labels - from https://kodi.wiki/view/InfoLabels#Weather_labels

General:
Location, Updated, WeatherProvider

Forecast:
Day[0-6].Title, 
Day[0-6].HighTemp, 
Day[0-6].LowTemp, 
Day[0-6].Outlook, 

"""


def bom_forecast(url_stem):

    forecast_url = f'http://www.bom.gov.au/places/{url_stem}/forecast/'

    try:
        r = requests.get(forecast_url)
        soup = BeautifulSoup(r.text, 'html.parser')

    except Exception as inst:
        # If we can't get and parse the page at all, might as well bail right out...
        log(f'Error requesting/souping weather page at {forecast_url}')
        raise

    for index, day in enumerate(soup.find_all('div', class_="day")):
        log(index)
        log(day)


###########################################################
# MAIN (only for unit testing outside of Kodi)

if __name__ == "__main__":

    url_stems_to_test = ['vic/ascot-vale']
    for url_stem in url_stems_to_test:
        log(f'Testing url stem [{url_stem}]')
        bom_forecast(url_stem)