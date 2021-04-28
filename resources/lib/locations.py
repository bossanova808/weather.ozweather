import xbmc
import xbmcgui
import requests

from resources.lib.weatherzone import *
from resources.lib.bom_locations import *
from resources.lib.bom_radar import *




def refresh_locations():
    """
    Get the user's location and radar code choices from the addon settings and set them as window properties
    """
    log("Refreshing locations from settings")
    location_setting1 = ADDON.getSetting('Location1')
    location_setting2 = ADDON.getSetting('Location2')
    location_setting3 = ADDON.getSetting('Location3')
    locations = 0
    if location_setting1 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location1', location_setting1)
    else:
        set_property(WEATHER_WINDOW, 'Location1')
    if location_setting2 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location2', location_setting2)
    else:
        set_property(WEATHER_WINDOW, 'Location2')
    if location_setting3 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location3', location_setting3)
    else:
        set_property(WEATHER_WINDOW, 'Location3')
    # and set count of locations
    set_property(WEATHER_WINDOW, 'Locations', str(locations))

    log("Refreshing radar locations from settings")
    radar_setting1 = ADDON.getSetting('Radar1')
    radar_setting2 = ADDON.getSetting('Radar2')
    radar_setting3 = ADDON.getSetting('Radar3')
    radars = 0
    if radar_setting1 != '':
        radars += 1
        set_property(WEATHER_WINDOW, 'Radar1', radar_setting1)
    else:
        set_property(WEATHER_WINDOW, 'Radar1')
    if radar_setting2 != '':
        radars += 1
        set_property(WEATHER_WINDOW, 'Radar2', radar_setting2)
    else:
        set_property(WEATHER_WINDOW, 'Radar2')
    if radar_setting3 != '':
        radars += 1
        set_property(WEATHER_WINDOW, 'Radar3', radar_setting3)
    else:
        set_property(WEATHER_WINDOW, 'Radar3')
    # and set count of radars
    set_property(WEATHER_WINDOW, 'Radars', str(locations))


def find_bom_locations():
    """
    Find BOM location(s) when the user inputs a postcode or suburb
    What we need is actually a geohash we can then use with the BOM API
    Save the chosen result, e.g. Ascot Vale, VIC 3032 and geohash r1r11df
    """
    keyboard = xbmc.Keyboard('', LANGUAGE(32195), False)
    keyboard.doModal()

    if keyboard.isConfirmed() and keyboard.getText() != '':
        text = keyboard.getText()

        log("Doing locations search for " + text)
        locations, location_geohashes = get_bom_locations_for(text)

        # Now get them to choose an actual location from the returned matched
        dialog = xbmcgui.Dialog()

        # None  found?
        if not locations:
            dialog.ok(ADDON_NAME, xbmc.getLocalizedString(284))
        # Show the list, let the user choose
        else:
            selected = dialog.select(xbmc.getLocalizedString(396), locations)
            if selected != -1:
                # Get the full location info for the chosen geohash, notably lat & long
                # Don't save the settings is this goes wrong
                location_info_url = f'https://api.weather.bom.gov.au/v1/locations/{location_geohashes[selected]}'
                try:
                    location_info = requests.get(location_info_url).json()['data']
                    log(location_info)
                except:
                    log("Error retrieving location info for geohash {location_geohashes[selected]}")
                    raise

                # Save the geohash and latitude and longitude of the location
                ADDON.setSetting(sys.argv[1], locations[selected])
                ADDON.setSetting(sys.argv[1] + 'BOMGeoHash', location_geohashes[selected])
                ADDON.setSetting(sys.argv[1] + 'Lat', str(location_info['latitude']))
                ADDON.setSetting(sys.argv[1] + 'Lon', str(location_info['longitude']))
                # Use the lat, long to find the closest radar
                radar = closest_radar_to_lat_lon((location_info['latitude'], location_info['longitude']))
                log(f'Closest radar found: {radar}')
                ADDON.setSetting('Radar' + sys.argv[1][-1] + 'Lat', str(radar[0]))
                ADDON.setSetting('Radar' + sys.argv[1][-1] + 'Lon', str(radar[1]))




