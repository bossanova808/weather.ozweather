# -*- coding: utf-8 -*-
class Store:
    """
    Helper class to to provide a centralised store for CONSTANTS and globals
    """

    # Static class variables, referred to by Store.whatever
    # https://docs.python.org/3/faq/programming.html#how-do-i-create-static-class-data-and-static-class-methods

    # CONSTANTS
    # ABC WEATHER VIDEO - scraping
    ABC_URL = "https://www.abc.net.au/news/newschannel/weather-in-90-seconds/"
    ABC_WEATHER_VIDEO_PATTERN = "//abcmedia.akamaized.net/news/news24/wins/(.+?)/WIN(.*?)_512k.mp4"
    ABC_STUB = "https://abcmedia.akamaized.net/news/news24/wins/"
    # WEATHERZONE - scraping, only used as a fallback data source if BOM not configured or fails
    WEATHERZONE_URL = 'https://www.weatherzone.com.au'
    WEATHERZONE_SEARCH_URL = WEATHERZONE_URL + "/search/"
    # BOM - JSON API
    BOM_URL = 'http://www.bom.gov.au'
    BOM_API_URL = 'https://api.weather.bom.gov.au/v1'
    BOM_API_LOCATIONS_URL = BOM_API_URL + '/locations'
    # BOM - RADARS - FTP
    BOM_RADAR_FTPSTUB = "ftp://anonymous:someone%40somewhere.com@ftp.bom.gov.au//anon/gen/radar/"
    BOM_RADAR_BACKGROUND_FTPSTUB = "ftp://anonymous:someone%40somewhere.com@ftp.bom.gov.au//anon/gen/radar_transparencies/"
    BOM_RADAR_HTTPSTUB = "http://www.bom.gov.au/products/radar_transparencies/"
    # http://www.bom.gov.au/australia/radar/about/radar_site_info.shtml
    # Cross check with: https://github.com/theOzzieRat/bom-radar-card/blob/master/src/bom-radar-card.ts around line 130
    BOM_RADAR_LOCATIONS = [
        # NSW http://www.bom.gov.au/australia/radar/info/nsw_info.shtml
        (-35.661387, 149.512229, "IDR403", "Canberra (Captain's Flat)"),
        (-29.620633, 152.963328, "IDR283", "Grafton"),
        (-29.496994, 149.850825, "IDR533", "Moree"),
        (-31.024219, 150.192037, "IDR693", "Namoi (Blackjack Mountain)"),
        (-32.729802, 152.025422, "IDR043", "Newcastle"),
        (-33.700764, 151.209470, "IDR713", "Sydney (Terrey Hills)"),
        (-29.038524, 167.941679, "IDR623", "Norfolk Island"),
        (-35.158170, 147.456307, "IDR553", "Wagga Wagga"),
        (-34.262389, 150.875099, "IDR033", "Wollongong (Appin)"),
        # VIC http://www.bom.gov.au/australia/radar/info/vic_info.shtml
        (-37.855210, 144.755512, "IDR023", "Melbourne"),
        (-34.28, 141.59, "IDR973", "Mildura"),
        (-37.887532, 147.575475, "IDR683", "Bairnsdale"),
        (-35.990000, 142.010000, "IDR953", "Rainbow"),
        (-36.029663, 146.022772, "IDR493", "Yarrawonga"),
        # QLD http://www.bom.gov.au/australia/radar/info/qld_info.shtml
        (-19.885737, 148.075693, "IDR", ""),
        (-27.717739, 153.240015, "IDR", ""),
        (-16.818145, 145.662895, "IDR", ""),
        (-23.549558, 148.239166, "IDR", ""),
        (-23.855056, 151.262567, "IDR", ""),
        (-25.957342, 152.576898, "IDR", ""),
        (-23.439783, 144.282270, "IDR", ""),
        (-21.117243, 149.217213, "IDR", ""),
        (-27.606344, 152.540084, "IDR", ""),
        (-16.670000, 139.170000, "IDR", ""),
        (-20.711204, 139.555281, "IDR", ""),
        (-19.419800, 146.550974, "IDR", ""),
        (-26.440193, 147.349130, "IDR", ""),
        (-12.666413, 141.924640, "IDR", ""),
        (-16.287199, 149.964539, "IDR", ""),
        (-34.617016, 138.468782, "IDR", ""),
        (-43.112593, 147.805241, "IDR", ""),
        (-41.179147, 145.579986, "IDR", ""),
        (-23.795064, 133.888935, "IDR", ""),
        (-12.455933, 130.926599, "IDR", ""),
        (-12.274995, 136.819911, "IDR", ""),
        (-14.510918, 132.447010, "IDR", ""),
        (-11.648500, 133.379977, "IDR", ""),
        (-34.941838, 117.816370, "IDR", ""),
        (-17.948234, 122.235334, "IDR", ""),
        (-24.887978, 113.669386, "IDR", ""),
        (-20.653613, 116.683144, "IDR", ""),
        (-31.777795, 117.952768, "IDR", ""),
        (-33.830150, 121.891734, "IDR", ""),
        (-28.804648, 114.697349, "IDR", ""),
        (-25.033225, 128.301756, "IDR", ""),
        (-30.784261, 121.454814, "IDR", ""),
        (-22.103197, 113.999698, "IDR", ""),
        (-33.096956, 119.008796, "IDR", ""),
        (-32.391761, 115.866955, "IDR", ""),
        (-20.371845, 118.631670, "IDR", ""),
        (-30.358887, 116.305769, "IDR", ""),
        (-15.451711, 128.120856, "IDR", ""),
        (-35.329531, 138.502498, "IDR", ""),
        (-32.129823, 133.696361, "IDR", ""),
        (-37.747713, 140.774605, "IDR", ""),
        (-31.155811, 136.804400, "IDR", ""),
        (-18.228916, 127.662836, "IDR", ""),
        (-29.971116, 146.813845, "IDR933", "Brewarrina"),
    ]

    DAYS = {"Mon": "Monday",
            "Tue": "Tuesday",
            "Wed": "Wednesday",
            "Thu": "Thursday",
            "Fri": "Friday",
            "Sat": "Saturday",
            "Sun": "Sunday"}

    WEATHER_CODES = {'clearing_shower': '39',
                     'clear': '32',
                     'cloudy': '26',
                     'cloud_and_wind_increasing': '23',
                     'cloud_increasing': '26',
                     'drizzle': '11',
                     'drizzle_clearing': '39',
                     'fog': '20',
                     'fog_then_sunny': '34',
                     'frost_then_sunny': '34',
                     'hazy': '21',
                     'heavy_rain': '40',
                     'heavy_showers': '12',
                     'increasing_sunshine': '30',
                     'late_shower': '45',
                     'light_shower': '11',
                     'late_thunder': '47',
                     'mostly_cloudy': '26',
                     'mostly_sunny': '34',
                     'overcast': '26',
                     'possible_shower': '11',
                     'possible_thunderstorm': '37',
                     'rain': '40',
                     'rain_and_snow': '5',
                     'rain_clearing': '39',
                     'rain_developing': '12',
                     'rain_tending to_snow': '5',
                     'shower': '11',
                     'showers': '11',
                     'showers_easing': '11',
                     'showers_increasing': '11',
                     'snow': '41',
                     'snowfalls_clearing': '5',
                     'snow_developing': '13',
                     'snow_showers': '41',
                     'snow_tending to_rain': '5',
                     'storm': '38',
                     'sunny': '32',
                     'thunderstorms': '38',
                     'thunderstorms_clearing': '37',
                     'windy': '23',
                     'windy_with_rain': '2',
                     'windy_with_showers': '2',
                     'windy_with_snow': '43',
                     'wind_and_rain_increasing': '2',
                     'wind_and_showers_easing': '11',
                     'unknown': 'na',
                     'nt_unknown': 'na'}

    WEATHER_CODES_NIGHT = {'clearing_shower': '45',
                           'clear': '31',
                           'cloudy': '29',
                           'cloud_and_wind_increasing': '27',
                           'cloud_increasing': '27',
                           'drizzle': '45',
                           'drizzle_clearing': '45',
                           'fog': '20',
                           'fog_then_sunny': '33',
                           'frost_then_sunny': '33',
                           'hazy': '33',
                           'heavy_rain': '47',
                           'heavy_showers': '45',
                           'increasing_sunshine': '31',
                           'late_shower': '45',
                           'light_shower': '45',
                           'late_thunder': '47',
                           'mostly_cloudy': '27',
                           'mostly_sunny': '31',
                           'overcast': '29',
                           'possible_shower': '45',
                           'possible_thunderstorm': '47',
                           'rain': '45',
                           'rain_and_snow': '46',
                           'rain_clearing': '45',
                           'rain_developing': '45',
                           'rain_tending to_snow': '45',
                           'shower': '45',
                           'showers': '45',
                           'showers_easing': '45',
                           'showers_increasing': '45',
                           'snow': '46',
                           'snowfalls_clearing': '46',
                           'snow_developing': '46',
                           'snow_showers': '46',
                           'snow_tending to_rain': '46',
                           'storm': '47',
                           'sunny': '31',
                           'thunderstorms': '47',
                           'thunder-storms': '47',
                           'thunderstorms_clearing': '47',
                           'windy': '29',
                           'windy_with_rain': '45',
                           'windy_with_showers': '45',
                           'windy_with_snow': '46',
                           'wind_and_rain_increasing': '45',
                           'wind_and_showers_easing': '45',
                           'unknown': 'na',
                           'nt_unknown': 'na'}

    """
    These are the weather codes for Kodi it seems
    N/A Not Available
    0 Rain/Lightning
    01 Windy/Rain
    02 Same as 01
    03 Same as 00
    04 Same as 00
    05 Cloudy/Snow-Rain Mix
    06 Hail
    07 Icy/Clouds Rain-Snow
    08 Icy/Haze Rain
    09 Haze/Rain
    10 Icy/Rain
    11 Light Rain
    12 Moderate Rain
    13 Cloudy/Flurries
    14 Same as 13
    15 Flurries
    16 Same as 13
    17 Same as 00
    18 Same as 00
    19 Dust
    20 Fog
    21 Haze
    22 Smoke
    23 Windy
    24 Same as 23
    25 Frigid
    26 Mostly Cloudy
    27 Mostly Cloudy/Night
    28 Mostly Cloudy/Sunny
    29 Partly Cloudy/Night
    30 Partly Cloudy/Day
    31 Clear/Night
    32 Clear/Day
    33 Hazy/Night
    34 Hazy/Day
    35 Same as 00
    36 Hot!
    37 Lightning/Day
    38 Lightning
    39 Rain/Day
    40 Rain
    41 Snow
    42 Same as 41
    43 Windy/Snow
    44 Same as 30
    45 Rain/Night
    46 Snow/Night
    47 Thunder Showers/Night

    NIGHT SUBSET:
    27 Mostly Cloudy/Night
    29 Partly Cloudy/Night
    31 Clear/Night
    33 Hazy/Night
    45 Rain/Night
    46 Snow/Night
    47 Thunder Showers/Night
    """

    # Just a store!
    def __init__(self):
        pass

