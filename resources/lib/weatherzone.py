# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with KODI; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

# CONSTANTS

SCHEMA = "http://"
WEATHERZONE_URL = 'www.weatherzone.com.au'
WEATHERZONE_SEARCH_URL = WEATHERZONE_URL + "/search/"

DAYS = {    "Mon": "Monday",
            "Tue": "Tuesday",
            "Wed": "Wednesday",
            "Thu": "Thursday",
            "Fri": "Friday",
            "Sat": "Saturday",
            "Sun": "Sunday"}

WEATHER_CODES = {   'Clearing Shower'                 : '39',
                    'Cloudy'                          : '26',
                    'Cloud And Wind Increasing'       : '23',
                    'Cloud Increasing'                : '26',
                    'Drizzle'                         : '11',
                    'Drizzle Clearing'                : '39',
                    'Fog Then Sunny'                  : '34',
                    'Frost Then Sunny'                : '34',
                    'Hazy'                            : '21',
                    'Heavy Rain'                      : '40',
                    'Heavy Showers'                   : '12',
                    'Increasing Sunshine'             : '30',
                    'Late Shower'                     : '45',
                    'Late Thunder'                    : '47',
                    'Mostly Cloudy'                   : '26',
                    'Mostly Sunny'                    : '34',
                    'Overcast'                        : '26',
                    'Possible Shower'                 : '11',
                    'Possible Thunderstorm'           : '37',
                    'Rain'                            : '40',
                    'Rain And Snow'                   : '5',
                    'Rain Clearing'                   : '39',
                    'Rain Developing'                 : '12',
                    'Rain Tending To Snow'            : '5',
                    'Showers'                         : '11',
                    'Showers Easing'                  : '11',
                    'Showers Increasing'              : '11',
                    'Snow'                            : '41',
                    'Snowfalls Clearing'              : '5',
                    'Snow Developing'                 : '13',
                    'Snow Showers'                    : '41',
                    'Snow Tending To Rain'            : '5',
                    'Sunny'                           : '32',
                    'Thunderstorms'                   : '38',
                    'ThunderStorms'                   : '38',
                    'Thunderstorms Clearing'          : '37',
                    'Windy'                           : '23',
                    'Windy With Rain'                 : '2',
                    'Windy With Showers'              : '2',
                    'Windy With Snow'                 : '43',
                    'Wind And Rain Increasing'        : '2',
                    'Wind And Showers Easing'         : '11',
                    'Unknown'                         : 'na',
                    'nt_unknown'                      : 'na'}

"""   These are the weather codes for XBMC is seems
N/A Not Available
0 Rain/Lightning
01 Windy/Rain
02 Same as 01
03 Same as 00
04 Same as 00
05 Cloudy/Snow-Rain Mix
06 Hail
07 Icy/Clouds Rain-Snow
08 Icy/Haze Rain
09 Haze/Rain
10 Icy/Rain
11 Light Rain
12 Moderate Rain
13 Cloudy/Flurries
14 Same as 13
15 Flurries
16 Same as 13
17 Same as 00
18 Same as 00
19 Dust
20 Fog
21 Haze
22 Smoke
23 Windy
24 Same as 23
25 Frigid
26 Mostly Cloudy
27 Mostly Cloudy/Night
28 Mostly Cloudy/Sunny
29 Partly Cloudy/Night
30 Partly Cloudy/Day
31 Clear/Night
32 Clear/Day
33 Hazy/Night
34 Hazy/Day
35 Same as 00
36 Hot!
37 Lightning/Day
38 Lightning
39 Rain/Day
40 Rain
41 Snow
42 Same as 41
43 Windy/Snow
44 Same as 30
45 Rain/Night
46 Snow/Night
47 Thunder Showers/Night
"""



# Our global to hold the built up weather data
weatherData = {}

def fireDangerToText(fireDangerFloat):

    if 0.0 <= fireDangerFloat <= 5.99:
        fireDangerText = "Low"
    elif 6 <= fireDangerFloat <= 11.99:
        fireDangerText = "Moderate"
    elif 12.0 <= fireDangerFloat <= 24.99:
        fireDangerText = "High" 
    elif 25.0 <= fireDangerFloat <= 49.99:
        fireDangerText = "Very High" 
    elif 50.0 <= fireDangerFloat <= 74.99:
        fireDangerText = "Severe" 
    elif 75.0 <= fireDangerFloat <= 99.99:
        fireDangerText = "Extreme" 
    elif fireDangerFloat >= 100.0:
        fireDangerText = "Catastrophic" 
    else:
        fireDangerText = "?" 

    return fireDangerText


def cleanShortDescription(description):
    description = description.replace( '-<br />','')
    description = description.replace( '-<Br />','')
    description = description.replace( 'ThunderStorms','Thunderstorms')
    description = description.replace( 'windy','Windy')
    # title capatilises the first letter of each word
    return description.title()


# Returns an array of dicts, each with a Locationname and LocationUrlPart.  Empty if no location found.
# [{'LocationName': u'Ascot Vale, VIC 3032', 'LocationUrlPart': u'/vic/melbourne/ascot-vale'}, ... ]

def getLocationsForPostcodeOrSuburb(text):

    locations = []
    locationURLPaths = []

    try:
        r = requests.post(SCHEMA + WEATHERZONE_SEARCH_URL, data={'q' : text, 't' : '3' })
        soup = BeautifulSoup(r.text, 'html.parser')
        print("Result url: " + r.url)

    except Exception as inst:
        print("Exception loading locations results in weatherzone.getLocationsForPostcodeOrSuburb" + str(inst))
        raise
    
    # Two repsonses are possible.
    try:

        # 1. A list of possible locations to choose from (e.g. several suburbs sharing one postcode)
        if r.url.endswith(WEATHERZONE_SEARCH_URL):       
            locationUl = soup.find("ul", class_="typ2")
            
            # Results block missing? Short circuit
            if not locationUl:
                return locations, locationURLPaths
            
            for locationLi in locationUl.find_all("li"):
                location = locationLi.find("a")
                locations.append(location.text)
                locationURLPaths.append(location.get('href'))
            
        # 2. Straight to one location
        else:
            h1 = soup.find("h1", class_="local")
            name = h1.text.split(" Weather")[0]
            url = urlparse(r.url).path
            locations.append(name)
            locationURLPaths.append(url)

    except Exception as inst:
        print("Exception processing locations in weatherzone.getLocationsForPostcodeOrSuburb" + str(inst))
        raise

    return locations, locationURLPaths


def setKeys(index, keys, value):

    global weatherData

    for key in keys:
        if index is 0:
            weatherData['Current.' + key] = value
            weatherData['Current.' + key] = value

        weatherData['Day.' + str(index) + '.' + key] = value
        weatherData['Day.' + str(index) + '.' + key] = value
        weatherData['Daily.' + str(index+1) + '.' + key] = value
        weatherData['Daily.' + str(index+1) + '.' + key] = value

def setKey(index, key, value):

    global weatherData

    if index is 0:
        weatherData['Current.' + key] = value
        weatherData['Current.' + key] = value

    weatherData['Day.' + str(index) + '.' + key] = value
    weatherData['Day.' + str(index) + '.' + key] = value
    weatherData['Daily.' + str(index+1) + '.' + key] = value
    weatherData['Daily.' + str(index+1) + '.' + key] = value

# Returns a dict of weather data values

def getWeatherData(urlPath, extendedFeatures = True):

    try:
        r = requests.get(SCHEMA + WEATHERZONE_URL + urlPath)
        soup = BeautifulSoup(r.text, 'html.parser')

    except Exception as inst:
        print("Error requesting/souping weather page at " + SCHEMA + WEATHERZONE_URL + urlPath)


    # All the try/excepts to follow are gross - python needs ?? support.  
    # But let's not fail if one value is missing/malformed...

    # Current Conditions - split in to two sides
    try:
        
        divCurrentDetailsLHS = soup.find("div", class_="details_lhs")
        lhs = divCurrentDetailsLHS.find_all("td", class_="hilite")        
        # print(lhs)

        divCurrentDetailsRHS = soup.find("div", class_="details_rhs")
        rhs = divCurrentDetailsRHS.find_all("td", class_="hilite")        
        # print(rhs)

                
        # LHS
        try:
            weatherData["Current.Temperature"] = str(int(round(float(lhs[0].text[:-2]))))
        except:
            weatherData["Current.Temperature"] = "?"       
        try:
            weatherData["Current.DewPoint"] = str(int(round(float(lhs[1].text[:-2]))))
        except:
            weatherData["Current.DewPoint"] = "?"
        try:
            weatherData["Current.FeelsLike"] = str(int(round(float(lhs[2].text[:-2]))))
        except:
            weatherData["Current.FeelsLike"] = "?"
        try:
            weatherData["Current.Humidity"] = str(int(round(float(lhs[3].text[:-1]))))
        except:
            weatherData["Current.Humidity"] = "?"
        try:
            weatherData["Current.WindDirection"] = str(lhs[4].text.split(" ")[0])
            weatherData["Current.WindDegree"] = weatherData["Current.WindDirection"]
        except:
            weatherData["Current.WindDirection"] = "?"
            weatherData["Current.WindDegree"] = "?"
        try:    
            weatherData["Current.Wind"] = str(lhs[4].text.split(" ")[1][:-4])
        except:
            weatherData["Current.Wind"] = "?"
        try:
            weatherData["Current.WindGust"] = str(lhs[5].text[:-4])
        except:
            weatherData["Current.WindGust"] = "?"
        try:
            weatherData["Current.Pressure"] = str(lhs[6].text[:-3])
        except:
            weatherData["Current.Pressure"] = "?"
        try:
            weatherData["Current.FireDanger"] = str(float(lhs[7].text))
        except:
            weatherData["Current.FireDanger"] = "?"
        try:
            weatherData["Current.FireDangerText"] = fireDangerToText(float(lhs[7].text))
        except:
            weatherData["Current.FireDangerText"] = "?"
        try:
            rainSince = lhs[8].text.partition('/')
            weatherData["Current.RainSince9am"] = str(rainSince[0][:-3])
            weatherData["Current.Precipitation"] = str(weatherData["Current.RainSince9am"])
            if rainSince[2] == " -":
                weatherData["Current.RainLastHr"] = "0"
            else:
                weatherData["Current.RainLastHr"] = str(rainSince[2][:-2])   
        except:
            weatherData["Current.RainSince9am"] = "?"
            weatherData["Current.Precipitation"] = "?"
            weatherData["Current.RainLastHr"] = "?"

        # RHS
        try:
            weatherData['Today.Sunrise'] = rhs[0].text
            weatherData['Today.Sunset'] = rhs[1].text
        except:
            weatherData['Today.Sunrise'] = "?"
            weatherData['Today.Sunset'] = "?"

    except Exception as inst:
        print("Exception processing current conditions data from " + SCHEMA + WEATHERZONE_URL + urlPath + "\n" + str(inst))
        raise
       

    # @TODO Next 12 Hours
    # try:        
    # except Exception as inst:
    #     print("Exception processing next 12 hour forecast data from " + SCHEMA + WEATHERZONE_URL + urlPath + "\n" + str(inst))
    #     raise


    # 7 Day Forecast

    try:
        forecastTable = soup.find("table", id="forecast-table")
        
        for index, row in enumerate(forecastTable.find_all("tr")):
            
            # Days and dates
            if index is 0:
                for i, day in enumerate(row.find_all("span", class_="bold")):
                    fullDay = DAYS[day.text]

                    setKey(i, "ShortDay", day.text)
                    setKey(i, "Title", fullDay)

                for i, date in enumerate(row.find_all("span", class_="text_blue")):
                    setKey(i, "ShortDate", date.text[3:])
    
            
            # Outlook = Short Descriptions & Corresponding Icons
            if index is 1:
                for i, shortDesc in enumerate(row.find_all("span")):

                    setKey(i, "Outlook", cleanShortDescription(shortDesc.text))
                    setKey(i, "Condition", cleanShortDescription(shortDesc.text))

                    try:
                        weathercode = WEATHER_CODES[cleanShortDescription(shortDesc.text)]
                    except:
                        weathercode = 'na'
                    value = '%s.png' % weathercode
                    setKeys(i, ["OutlookIcon","ConditionIcon"], value)


            # Maximums
            if index is 2:
                for i, td in enumerate(row.find_all("td")):
 
                    value = '%s' % td.text[:-2]
                    setKeys(i, ["HighTemp","HighTemperature"], value)
 
            # Minimums
            if index is 3:
                for i, td in enumerate(row.find_all("td")):

                    value = '%s' % td.text[:-2]

                    value = '%s' % td.text[:-2]
                    setKeys(i, ["LowTemp","LowTemperature"], value)

            # Chance of rain
            if index is 4:
                for i, td in enumerate(row.find_all("td")):

                    value = '%s' % td.text[:-1]
                    setKey(i, "ChancePrecipitation", value)

            # Amount of rain
            if index is 5:
                for i, td in enumerate(row.find_all("td")):

                    value = '%s' % td.text
                    setKey(i, "Precipitation", value)


            # print "\n\n" + str(index)
            # print row

        # Moonphase
        try:
            astronomyTable = soup.find("table", class_="astronomy")
            tds = astronomyTable.find_all("td")
            value = tds[4].find("img").get('title').title()
            weatherData['Today.moonphase'] = value
            weatherData['Today.Moonphase'] = value

        except Exception as inst:
            print("Exception processing moonphase data from " + SCHEMA + WEATHERZONE_URL + urlPath + "\n" + str(inst))
            raise


    except Exception as inst:
        print("Exception processing forecast rows data from " + SCHEMA + WEATHERZONE_URL + urlPath + "\n" + str(inst))
        raise



    return weatherData


###########################################################
# MAIN - for testing outside of Kodi

if __name__ == "__main__":
    print("\n\nTesting scraping of Weatherzone\n")

    print("First test getting weatherzone location from postcode/suburb name:");

    print("\n3032:")
    print(getLocationsForPostcodeOrSuburb(3032))
    print("\n9999:")
    print(getLocationsForPostcodeOrSuburb(9999))
    print("\nKyneton:")
    print(getLocationsForPostcodeOrSuburb("Kyneton"))

    print("\n\nGet weather data for /vic/central/kyneton:")
    weatherData = getWeatherData("/vic/central/kyneton", True)

    for key in sorted(weatherData):
        print "%s: %s" % (key, weatherData[key])
