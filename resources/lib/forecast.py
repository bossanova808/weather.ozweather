from resources.lib.weatherzone.weatherzone_forecast import *
from resources.lib.abc.abc_video import *
from resources.lib.bom.bom_radar import *
from resources.lib.bom.bom_forecast import *


def clear_properties():
    """
    Clear all properties on the weather window in preparation for an update.
    """
    log("Clearing all weather window properties")
    try:
        set_property(WEATHER_WINDOW, 'WeatherProviderLogo')
        set_property(WEATHER_WINDOW, 'WeatherProvider')
        set_property(WEATHER_WINDOW, 'WeatherVersion')
        set_property(WEATHER_WINDOW, 'Location')
        set_property(WEATHER_WINDOW, 'Updated')
        set_property(WEATHER_WINDOW, 'Weather.IsFetched', "false")
        set_property(WEATHER_WINDOW, 'Daily.IsFetched', "false")
        set_property(WEATHER_WINDOW, 'Radar')
        set_property(WEATHER_WINDOW, 'Video.1')

        set_property(WEATHER_WINDOW, 'Forecast.City')
        set_property(WEATHER_WINDOW, 'Forecast.Country')
        set_property(WEATHER_WINDOW, 'Forecast.Updated')

        set_property(WEATHER_WINDOW, 'Current.IsFetched', "false")
        set_property(WEATHER_WINDOW, 'Current.Location')
        set_property(WEATHER_WINDOW, 'Current.Condition')
        set_property(WEATHER_WINDOW, 'Current.ConditionLong')
        set_property(WEATHER_WINDOW, 'Current.Temperature')
        set_property(WEATHER_WINDOW, 'Current.Wind')
        set_property(WEATHER_WINDOW, 'Current.WindDirection')
        set_property(WEATHER_WINDOW, 'Current.WindDegree')
        set_property(WEATHER_WINDOW, 'Current.WindGust')
        set_property(WEATHER_WINDOW, 'Current.Pressure')
        set_property(WEATHER_WINDOW, 'Current.FireDanger')
        set_property(WEATHER_WINDOW, 'Current.FireDangerText')
        set_property(WEATHER_WINDOW, 'Current.Visibility')
        set_property(WEATHER_WINDOW, 'Current.Humidity')
        set_property(WEATHER_WINDOW, 'Current.FeelsLike')
        set_property(WEATHER_WINDOW, 'Current.DewPoint')
        set_property(WEATHER_WINDOW, 'Current.UVIndex')
        set_property(WEATHER_WINDOW, 'Current.OutlookIcon', "na.png")
        set_property(WEATHER_WINDOW, 'Current.ConditionIcon', "na.png")
        set_property(WEATHER_WINDOW, 'Current.FanartCode')
        set_property(WEATHER_WINDOW, 'Current.Sunrise')
        set_property(WEATHER_WINDOW, 'Current.Sunset')
        set_property(WEATHER_WINDOW, 'Current.RainSince9')
        set_property(WEATHER_WINDOW, 'Current.RainLastHr')
        set_property(WEATHER_WINDOW, 'Current.Precipitation')
        set_property(WEATHER_WINDOW, 'Current.ChancePrecipitation')
        set_property(WEATHER_WINDOW, 'Current.SolarRadiation')

        set_property(WEATHER_WINDOW, 'Today.IsFetched', "false")
        set_property(WEATHER_WINDOW, 'Today.Sunrise')
        set_property(WEATHER_WINDOW, 'Today.Sunset')
        set_property(WEATHER_WINDOW, 'Today.moonphase')
        set_property(WEATHER_WINDOW, 'Today.Moonphase')

        # and all the properties for the forecast
        for count in range(0, 14):
            set_property(WEATHER_WINDOW, 'Day%i.Title' % count)
            set_property(WEATHER_WINDOW, 'Day%i.RainChance' % count)
            set_property(WEATHER_WINDOW, 'Day%i.RainChanceAmount' % count)
            set_property(WEATHER_WINDOW, 'Day%i.ChancePrecipitation' % count)
            set_property(WEATHER_WINDOW, 'Day%i.Precipitation' % count)
            set_property(WEATHER_WINDOW, 'Day%i.HighTemp' % count)
            set_property(WEATHER_WINDOW, 'Day%i.LowTemp' % count)
            set_property(WEATHER_WINDOW, 'Day%i.HighTemperature' % count)
            set_property(WEATHER_WINDOW, 'Day%i.LowTemperature' % count)
            set_property(WEATHER_WINDOW, 'Day%i.Outlook' % count)
            set_property(WEATHER_WINDOW, 'Day%i.LongOutlookDay' % count)
            set_property(WEATHER_WINDOW, 'Day%i.OutlookIcon' % count, "na.png")
            set_property(WEATHER_WINDOW, 'Day%i.ConditionIcon' % count, "na.png")
            set_property(WEATHER_WINDOW, 'Day%i.FanartCode' % count)
            set_property(WEATHER_WINDOW, 'Day%i.ShortDate' % count)
            set_property(WEATHER_WINDOW, 'Day%i.ShortDay' % count)

            set_property(WEATHER_WINDOW, 'Daily.%i.Title' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.RainChance' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.RainChanceAmount' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.ChancePrecipitation' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.Precipitation' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.HighTemp' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.LowTemp' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.HighTemperature' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.LowTemperature' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.Outlook' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.LongOutlookDay' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.OutlookIcon' % count, "na.png")
            set_property(WEATHER_WINDOW, 'Daily.%i.ConditionIcon' % count, "na.png")
            set_property(WEATHER_WINDOW, 'Daily.%i.FanartCode' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.ShortDate' % count)
            set_property(WEATHER_WINDOW, 'Daily.%i.ShortDay' % count)

    except Exception as inst:
        log("********** Oz Weather Couldn't clear all the properties, sorry!!", inst)


def forecast(geohash, url_path, radar_code):
    """
    The main weather data retrieval function
    Does either a basic forecast, or a more extended forecast with radar etc.
    :param geohash: the BOM geohash for the location
    :param url_path: the WeatherZone url path if still using that...
    :param radar_code: the BOM radar code (e.g. 'IDR063') to retrieve the radar loop for
    """
    extended_features = ADDON.getSetting('ExtendedFeaturesToggle')
    log(f'Extended features: {extended_features}')

    # Get the radar images first - because it looks better on refreshes
    if extended_features == "true":
        log(f'Getting radar images for {radar_code}')

        backgrounds_path = xbmcvfs.translatePath(
            "special://profile/addon_data/weather.ozweather/radarbackgrounds/" + radar_code + "/");
        overlay_loop_path = xbmcvfs.translatePath(
            "special://profile/addon_data/weather.ozweather/currentloop/" + radar_code + "/");

        # Do they want us to periodically refresh radar backgrounds?  Default is yes...
        # (this was added as some folks has issues and manually copied the backgrounds in....)
        update_radar_backgrounds = ADDON.getSetting('BGDownloadToggle')

        build_images(radar_code, update_radar_backgrounds, backgrounds_path, overlay_loop_path)
        set_property(WEATHER_WINDOW, 'Radar', radar_code)

    # Get all the weather & forecast data from the BOM API, fall back to weatherzone if there's issues...
    if geohash:
        log(f'Using the BOM API.  Getting weather data for {geohash}')
        weather_data = bom_forecast(geohash)

    if not weather_data and url_path:
        log(f'FALLBACK - Scraping Weatherzone.  Using url_path {url_path}. '
            f'User is encouraged to re-configure the addon as WeatherZone support will later be removed.')
        weather_data = getWeatherData(url_path)

    # At this point, we should have _something_ - if not, log the issue and we're done...
    if not weather_data:
        log_info("Unable to get weather_data from BOM or from Weatherzone - internet connection issue or addon not configured?")
        return

    # We have weather_data - set all the properties on Kodi's weather window...
    for weather_key in sorted(weather_data):
        set_property(WEATHER_WINDOW, weather_key, weather_data[weather_key])

    # Get the ABC 90 second weather video link if extended features is enabled
    if extended_features == "true":
        log("Getting the ABC weather video link")
        url = getABCWeatherVideoLink(ADDON.getSetting("ABCQuality"))
        if url:
            set_property(WEATHER_WINDOW, 'Video.1', url)

    # And announce everything is fetched..
    set_property(WEATHER_WINDOW, "Weather.IsFetched", "true")
    set_property(WEATHER_WINDOW, 'Forecast.Updated', time.strftime("%d/%m/%Y %H:%M"))
    set_property(WEATHER_WINDOW, 'Today.IsFetched', "true")


def get_weather():
    """
    Get the latest forecast data for the currently chosen location
    """

    # Nice neat updates - clear out all set window data first...
    clear_properties()

    # Set basic properties/'brand'
    set_property(WEATHER_WINDOW, 'WeatherProviderLogo', xbmcvfs.translatePath(os.path.join(CWD, 'resources', 'banner.png')))
    set_property(WEATHER_WINDOW, 'WeatherProvider', 'Bureau of Meteorology Australia')
    set_property(WEATHER_WINDOW, 'WeatherVersion', ADDON_NAME + "-" + ADDON_VERSION)

    # Set what we updated and when
    set_property(WEATHER_WINDOW, 'Location', ADDON.getSetting('Location%s' % sys.argv[1]))
    set_property(WEATHER_WINDOW, 'Updated', time.strftime("%d/%m/%Y %H:%M"))
    set_property(WEATHER_WINDOW, 'Current.Location', ADDON.getSetting('Location%s' % sys.argv[1]))
    set_property(WEATHER_WINDOW, 'Forecast.City', ADDON.getSetting('Location%s' % sys.argv[1]))
    set_property(WEATHER_WINDOW, 'Forecast.Country', "Australia")
    set_property(WEATHER_WINDOW, 'Forecast.Updated', time.strftime("%d/%m/%Y %H:%M"))

    # Retrieve the currently chosen location geohash, backup weatherzone url_path, & radar code
    geohash = ADDON.getSetting(f'Location{sys.argv[1]}BOMGeoHash')
    url_path = ADDON.getSetting(f'Location{sys.argv[1]}UrlPath')
    radar = ADDON.getSetting(f'Radar{sys.argv[1]}')
    # If we don't have a radar code, get the national radar by default
    if not radar:
        radar = 'IDR00004'
        log(f'Radar code empty for location, so using default radar code {radar} (= national radar)')

    log(f'Current location: geohash "{geohash}", urlpath "{url_path}", radar {radar}')

    # Now scrape the weather data & radar images
    forecast(geohash, url_path, radar)
