from .common import *
import requests


def get_bom_locations_for(text):

    bom_locations_api = 'https://api.weather.bom.gov.au/v1/locations'
    locations = []
    location_geohashes = []

    try:
        r = requests.get(bom_locations_api, params={'search': text})
        for result in r.json()['data']:
            log(result)
            locations.append(f'{result["name"]}, {result["state"]} {result["postcode"]} ({result["geohash"]})')
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


"""
{
    "data": {
        "geohash": "r659gg5", 
        "has_wave": true, 
        "id": "Gosford-r659gg5", 
        "latitude": -33.42521667480469, 
        "longitude": 151.3414764404297, 
        "marine_area_id": "NSW_MW009", 
        "name": "Gosford", 
        "state": "NSW", 
        "tidal_point": "NSW_TP036", 
        "timezone": "Australia/Sydney"
    }, 
    "metadata": {
        "response_timestamp": "2021-04-28T04:50:20Z"
    }
}
"""