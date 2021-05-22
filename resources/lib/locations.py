from resources.lib.common import *


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

