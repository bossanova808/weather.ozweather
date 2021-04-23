from common import *
import requests


def get_bom_locations_for(text):

    bom_locations_api = 'https://api.weather.bom.gov.au/v1/locations'
    locations = []
    location_geohashes = []

    try:
        r = requests.get(bom_locations_api, params={'search': text})
        for result in r.json()['data']:
            locations.append(f'{result["name"]}, {result["state"]} {result["postcode"]}')
            location_geohashes.append(result["geohash"])

        log(locations)
        log(location_geohashes)

        return locations, location_geohashes

    except Exception as inst:
        log(f'Exception getting locations from {bom_locations_api} for search term {text}')
        log(str(inst))
        raise


###########################################################
# MAIN (only for unit testing outside of Kodi)

if __name__ == "__main__":

    places_to_test = ['3032', 'ascot vale', 'MYRTLE BANK', 'no_results']
    for place in places_to_test:
        log(f'Testing location term "{place}"')
        get_bom_locations_for(place)
        log('')
