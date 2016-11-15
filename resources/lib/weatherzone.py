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

SCHEMA = "http://"
WEATHERZONE_URL = 'www.weatherzone.com.au'
WEATHERZONE_SEARCH_URL = WEATHERZONE_URL + "/search/"


def fireDangerToText(fireDangerFloat):

    if 0.0 <= fireDangerFloat <= 11.99:
        fireDangerText = "Low - Moderate"
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


# Returns a dict of weather data values

def getWeatherData(urlPath, extendedFeatures = True):

    weatherData = {}

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
            weatherData["Temperature"] = str(int(round(float(lhs[0].text[:-2]))))
        except:
            pass       
        try:
            weatherData["DewPoint"] = str(int(round(float(lhs[1].text[:-2]))))
        except:
            pass
        try:
            weatherData["FeelsLike"] = str(int(round(float(lhs[2].text[:-2]))))
        except:
            pass
        try:
            weatherData["Humidity"] = str(int(round(float(lhs[3].text[:-1]))))
        except:
            pass
        try:
            weatherData["WindDirection"] = lhs[4].text.split(" ")[0]
            weatherData["WindDegree"] = weatherData["WindDirection"]
        except:
            pass
        try:    
            weatherData["Wind"] = lhs[4].text.split(" ")[1][:-4]
        except:
            pass
        try:
            weatherData["WindGust"] = lhs[5].text[:-4]
        except:
            pass
        try:
            weatherData["Pressure"] = lhs[6].text[:-3]
        except:
            pass
        try:
            weatherData["FireDanger"] = float(lhs[7].text)
        except:
            pass
        try:
            weatherData["FireDangerText"] = fireDangerToText(weatherData["fireDanger"])
        except:
            pass
        try:
            rainSince = lhs[8].text.partition('/')
            weatherData["RainSince9am"] = str(rainSince[0].strip())
            weatherData["Precipitation"] = weatherData["RainSince9am"]
            weatherData["RainLastHr"] = str(rainSince[2].strip())   
        except:
            pass

        # RHS

        try:
            weatherData['Sunrise'] = rhs[0].text
            weatherData['Sunset'] = rhs[1].text
        except:
            pass

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
            
            if index in [0]:
                continue
            
            # Short Descriptions
            if index is 1:
                for index, shortDesc in enumerate(row.find_all("span")):
                    weatherData['Day.' + str(index) + '.Outlook'] = shortDesc.text
                    weatherData['Daily.' + str(index) + '.Outlook'] = shortDesc.text

            # print "\n\n" + str(index)
            # print row



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

    print("\n\nGet weather data for Ascot Vale:")
    print(getWeatherData("/sa/adelaide/myrtle-bank", True))

