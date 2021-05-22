# -*- coding: utf-8 -*-
import socket

from resources.lib.forecast import *
from resources.lib.locations import *
from resources.lib.bom.bom_location import *
from resources.lib.weatherzone.weatherzone_location import *


def run(args):
    """
    This is 'main' basically.
    TWO MAJOR MODES - SETTINGS and FORECAST RETRIEVAL

    @param args: sys.argv is passed through to here...
    """

    footprints()
    socket.setdefaulttimeout(100)

    # SETTINGS
    # the addon is being called from the settings section where the user enters their postcodes
    if args[1].startswith('Location'):
        if args[1].endswith('WeatherZone'):
            find_weatherzone_location()
        else:
            find_bom_location()

    # FORECAST
    # script is being called in general use, not from the settings page
    # sys.argv[1] has the current location number, so get the currently selected location and grab it's forecast
    else:
        get_weather()

    # Refresh the locations
    refresh_locations()

    # and close out...
    footprints(startup=False)
