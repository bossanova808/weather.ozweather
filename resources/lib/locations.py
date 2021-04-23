import xbmc
import xbmcgui

from resources.lib.weatherzone import *
from resources.lib.bom_locations import *


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

        # Now get them to choose an actual location
        dialog = xbmcgui.Dialog()
        if locations:
            selected = dialog.select(xbmc.getLocalizedString(396), locations)
            if selected != -1:
                ADDON.setSetting(sys.argv[1], locations[selected])
                ADDON.setSetting(sys.argv[1] + 'BOMGeoHash', location_geohashes[selected])
        # Or indicate we did not receive any locations
        else:
            dialog.ok(ADDON_NAME, xbmc.getLocalizedString(284))


# def find_bom_location():
#     """
#     Find a location (= BOM url path) - when the user inputs a postcode or suburb
#     """
#
#     keyboard = xbmc.Keyboard('', LANGUAGE(32195), False)
#     keyboard.doModal()
#
#     if keyboard.isConfirmed() and keyboard.getText() != '':
#         text = keyboard.getText()
#
#         log(f'Query BOM locations API for {text}')
#         places = get_bom_locations_for(text)
