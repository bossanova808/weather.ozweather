from common import *
import requests
from bs4 import BeautifulSoup


def get_bom_places_for(text):

    locations = []
    location_url_stems = []

    bom_url = 'http://www.bom.gov.au'
    bom_places_url = f'{bom_url}/onboarding'

    # Search for 'test' in BOM places:
    # http://www.bom.gov.au/places/search/?q=test
    # If the BOM finds only one match - it returns the full place url
    # E.g. search for 'ascot vale' ->  http://www.bom.gov.au/places/vic/ascot-vale/
    # If it finds more matches you get the searchr results page
    # E.g. search for 'myrtle bank' -> http://www.bom.gov.au/places/search/?q=myrtle+bank

    try:
        r = requests.post(bom_places_url, params={'q': text})
        soup = BeautifulSoup(r.text, 'html.parser')
        log(f'Search BOM places for {text}, result url is {r.url}')

        # Single result
        if 'search' not in r.url:
            # First h1
            place_name = soup.find_all('h1')[0].text
            cut_at = -8
            # Currently the BOM are calling this all beta, all over the place...
            if ' (beta)' in place_name:
                cut_at = -15
            place_name = place_name[:cut_at]
            locations.append(place_name)
            location_url_stems.append(r.url[len(bom_url):-1])

        # Multiple results
        else:
            search_results_ol = soup.find('ol', class_='search-results')
            anchors = search_results_ol.find_all('a')
            for anchor in anchors:
                locations.append(anchor.text)
                location_url_stems.append(anchor["href"][:-1])

        log("Found places:")
        log(locations)
        log(location_url_stems)

        return locations, location_url_stems

    except Exception as inst:
        log("Exception loading locations results in weatherzone.getLocationsForPostcodeOrSuburb" + str(inst))
        raise


###########################################################
# MAIN (only for unit testing outside of Kodi)

if __name__ == "__main__":

    places_to_test = ['3032', 'ascot vale', 'myrtle bank']
    for place in places_to_test:
        log(f'Testing place [{place}]')
        get_bom_places_for(place)