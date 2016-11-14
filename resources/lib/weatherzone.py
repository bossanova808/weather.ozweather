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

from logger import *


SCHEMA = "http://"
WEATHERZONE_URL = 'www.weatherzone.com.au'
WEATHERZONE_SEARCH_URL = WEATHERZONE_URL + "/search/"



# Returns :
# [] 
# [{'LocationName': u'Ascot Vale, VIC 3032', 'LocationUrlPart': u'/vic/melbourne/ascot-vale'}, {'LocationName': u'Maribyrnong, VIC 3032', 'LocationUrlPart': u'/vic/melbourne/maribyrnong'}, {'LocationName': u'Travancore, VIC 3032', 'LocationUrlPart': u'/vic/melbourne/travancore'}, {'LocationName': u'Highpoint City, VIC 3032', 'LocationUrlPart': u'/vic/melbourne/highpoint-city'}]

def getLocationsForPostcodeOrSuburb(text):

    results = []

    try:
        r = requests.post(SCHEMA + WEATHERZONE_SEARCH_URL, data={'q' : text, 't' : '3' })
        soup = BeautifulSoup(r.text, 'html.parser')

        log("Result url: " + r.url)

        #Two repsonses are possible.
        # 1. A list of possible locations to choose from (e.g. several suburbs sharing one postcode)
        if r.url.endswith(WEATHERZONE_SEARCH_URL):       
            locationUl = soup.find("ul", class_="typ2")
            if not locationUl:
                return results
            for locationLi in locationUl.find_all("li"):
                location = locationLi.find("a")
                results.append({'LocationName':location.text, 'LocationUrlPath':location.get('href')})
            
        # 2. Straight to one location
        else:
            h1 = soup.find("h1", class_="local")
            name = h1.text.split(" Weather")[0]
            url = urlparse(r.url).path
            results.append({'LocationName':name, 'LocationUrlPath':url})

    except Exception as inst:
        log("Exception in weatherzone.getLocationsForPostcodeOrSuburb" + str(inst))
        raise

    return results

###########################################################
# MAIN

if __name__ == "__main__":
    print("\n\nTesting scraping of Weatherzone\n")

    print("First test getting weatherzone location from postcode/suburb name:");

    log("\n\n3032:")
    log(getLocationsForPostcodeOrSuburb(3032))
    log("\n\n9999:")
    log(getLocationsForPostcodeOrSuburb(9999))
    log("\n\nKyneton:")
    log(getLocationsForPostcodeOrSuburb("Kyneton"))


