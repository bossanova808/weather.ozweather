from .common import *


def refresh_locations():
    """
    Get the user's location and radar code choices from the addon settings, and set them as window properties
    """
    log("Refreshing locations from settings")

    location_setting1 = ADDON.getSetting('Location1BOM')
    location_fallback1 = ADDON.getSetting('Location1WeatherZone')
    location_setting2 = ADDON.getSetting('Location2BOM')
    location_fallback2 = ADDON.getSetting('Location2WeatherZone')
    location_setting3 = ADDON.getSetting('Location3BOM')
    location_fallback3 = ADDON.getSetting('Location3WeatherZone')

    locations = 0

    log("location_setting1: " + location_setting1)
    log("location_fallback1: " + location_fallback1)
    log("location_setting2: " + location_setting2)
    log("location_fallback2: " + location_fallback2)
    log("location_setting3: " + location_setting3)
    log("location_fallback3: " + location_fallback3)

    # If either the main location or the fall back is set, then enable the location
    # This is to cope with the transition period where folks will have the fallbacks set from their legacy settings
    # But not the new BOM locations
    if location_setting1 != '' or location_fallback1 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location1', location_setting1 or location_fallback1)
    else:
        set_property(WEATHER_WINDOW, 'Location1')
    if location_setting2 != '' or location_fallback2 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location2', location_setting2 or location_fallback2)
    else:
        set_property(WEATHER_WINDOW, 'Location2')
    if location_setting3 != '' or location_fallback3 != '':
        locations += 1
        set_property(WEATHER_WINDOW, 'Location3', location_setting3 or location_fallback3)
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

