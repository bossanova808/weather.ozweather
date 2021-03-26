import requests
import re
from bs4 import BeautifulSoup
from common import *

"""
Kodi Weather Info Labels - from https://kodi.wiki/view/InfoLabels#Weather_labels

General:
Location, Updated, WeatherProvider

Observations:
Current.Condition, 
Current.Temperature, 
Current.FeelsLike, 
Current.UVIndex, 
Current.Wind (From <wind dir.> at <speed> <unit>), 
Current.WindSpeed, 
Current.WindDirection, 
Current.DewPoint, 
Current.Humidity,
"""

