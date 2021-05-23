# -*- coding: utf-8 -*-
import datetime
import sys
import requests
import xbmc

# Small hack to allow for unit testing - see common.py for explanation
if not xbmc.getUserAgent():
    sys.path.insert(0, '../../..')

from resources.lib.store import Store
from resources.lib.common import *

"""
(See bottom of this file for BOM API examples)
"""


# This is a hack fix for a wicked long standing Python bug...
# See: https://forum.kodi.tv/showthread.php?tid=112916
class ProxyDatetime(datetime.datetime):
    @staticmethod
    def strptime(date_string, format):
        import time
        return datetime.datetime(*(time.strptime(date_string, format)[0:6]))


datetime.datetime = ProxyDatetime


def set_key(weather_data, index, key, value):
    """
    Set a key - for old and new weather label support
    """

    value = str(value)

    if index == 0:
        weather_data['Current.' + key] = value.strip()
        weather_data['Current.' + key] = value.strip()

    weather_data['Day' + str(index) + '.' + key] = value.strip()
    weather_data['Day' + str(index) + '.' + key] = value.strip()
    weather_data['Daily.' + str(index + 1) + '.' + key] = value.strip()
    weather_data['Daily.' + str(index + 1) + '.' + key] = value.strip()


def set_keys(weather_data, index, keys, value):
    """
    Set a group of keys at once - for old and new weather label support
    """
    for key in keys:
        set_key(weather_data, index, key, value)


def utc_str_to_local_datetime(utc_str: str, utc_format: str = '%Y-%m-%dT%H:%M:%SZ'):
    """
    Given a UTC string, return a datetime in the local timezone

    :param utc_str: UTC time string
    :param utc_format: format of UTC time string
    :param local_format: format of local time string
    :return: local time string
    """

    temp1 = datetime.datetime.strptime(utc_str, utc_format)
    temp2 = temp1.replace(tzinfo=datetime.timezone.utc)
    return temp2.astimezone()


def utc_str_to_local_str(utc_str: str, utc_format: str = '%Y-%m-%dT%H:%M:%SZ', local_format: str = '%I:%M %p'):
    """
    Given a UTC string, return a string with the local time in the given format

    :param utc_str: UTC time string
    :param utc_format: format of UTC time string
    :param local_format: format of local time string
    :return: local time string
    """
    local_time = utc_str_to_local_datetime(utc_str, utc_format)
    return local_time.strftime(local_format).lstrip('0')


def bom_forecast(geohash):
    """
    Return are information, current observations, warnings, and forecast for the given geohash
    If we're unable to get the key data (current observations and forecast) then return False
    ...will then fall back to scraping Weatherzone (if that is configured).

    :param: geohash - the BOM location geohash
    """

    # The areahash is the geohash minus the last character
    areahash = geohash[:-1]

    bom_api_url_geohash = f'{Store.BOM_API_LOCATIONS_URL}/{geohash}'
    bom_api_url_areahash = f'{Store.BOM_API_LOCATIONS_URL}/{areahash}'

    bom_api_area_information_url = bom_api_url_geohash
    bom_api_warnings_url = f'{bom_api_url_geohash}/warnings'

    bom_api_current_observations_url = f'{bom_api_url_areahash}/observations'
    bom_api_forecast_seven_days_url = f'{bom_api_url_areahash}/forecasts/daily'
    # FUTURE? - not yet used...
    bom_api_forecast_three_hourly_url = f'{bom_api_url_areahash}/forecasts/3-hourly'
    bom_api_forecast_rain = f'{bom_api_url_areahash}/forecast/rain'

    # Get the area information
    try:
        r = requests.get(bom_api_area_information_url)
        area_information = r.json()["data"]
        log(area_information)

    except Exception as inst:
        log(f'Error retrieving area information from {bom_api_area_information_url}')

    # Get current observations
    try:
        r = requests.get(bom_api_current_observations_url)
        current_observations = r.json()["data"]
        log(current_observations)

    except Exception as inst:
        log(f'Error retrieving current observations from {bom_api_current_observations_url}')
        return False

    # Get warnings
    try:
        r = requests.get(bom_api_warnings_url)
        warnings = r.json()["data"]
        log(warnings)

    except Exception as inst:
        log(f'Error retrieving warnings from {bom_api_warnings_url}')

    # Get 7 day forecast
    try:
        r = requests.get(bom_api_forecast_seven_days_url)
        forecast_seven_days = r.json()["data"]
        log(forecast_seven_days)

    except Exception as inst:
        log(f'Error retrieving seven day forecast from {bom_api_forecast_seven_days_url}')
        return False

    # FUTURE?
    # # Get 3 Hourly Forecast
    # try:
    #     r = requests.get(bom_api_forecast_three_hourly_url)
    #     forecast_three_hourly = r.json()["data"]
    #     log(forecast_three_hourly)
    #
    # except Exception as inst:
    #     log(f'Error retrieving three hourly forecast from {bom_api_forecast_three_hourly_url}')
    #     raise
    #
    # # Get Rain Forecast
    # try:
    #     r = requests.get(bom_api_forecast_rain)
    #     forecast_rain = r.json()["data"]
    #     log(forecast_rain)
    #
    # except Exception as inst:
    #     log(f'Error retrieving rain forecast from {bom_api_forecast_rain}')
    #     raise

    log('')

    # Gather the weather data into Kodi friendly labels
    weather_data = {}

    # Current Observations
    if current_observations:
        weather_data['Current.Temperature'] = str(round(current_observations['temp']))
        weather_data['Current.FeelsLike'] = str(round(current_observations['temp_feels_like']))
        weather_data['Current.Humidity'] = current_observations['humidity']
        weather_data['Current.WindSpeed'] = current_observations['wind']['speed_kilometre']
        weather_data['Current.WindDirection'] = current_observations['wind']['direction']
        weather_data['Current.Wind'] = f'From {current_observations["wind"]["direction"]} at {current_observations["wind"]["speed_kilometre"]} km/h'
        weather_data['Current.WindGust'] = f'{current_observations["gust"]["speed_kilometre"]}'
        weather_data["Current.Precipitation"] = weather_data["Current.RainSince9"] = f'{current_observations["rain_since_9am"]} mm'

    # Warnings
    warnings_text = ""

    if warnings:
        for i, warning in enumerate(warnings):
            warning_issued = utc_str_to_local_str(warning['issue_time'])
            # Time signature on the expiry is different for some reason?!
            # Remove the completely unnecessary fractions of a second...
            warning_expires = utc_str_to_local_str(warning['expiry_time'].replace('.000Z', 'Z'))
            warning_text = f'** {warning["title"]} (issued at {warning_issued}, expires {warning_expires}) **'
            warnings_text += warning_text
            if i != len(warnings):
                warnings_text += '\n\n'

    weather_data['Current.WarningsText'] = warnings_text

    # 7 Day Forecast
    if forecast_seven_days:
        weather_data['Current.Condition'] = forecast_seven_days[0]['short_text']
        weather_data['Current.ConditionLong'] = forecast_seven_days[0]['extended_text']
        weather_data['Current.Sunrise'] = weather_data['Today.Sunrise'] = utc_str_to_local_str(forecast_seven_days[0]['astronomical']['sunrise_time'])
        weather_data['Current.Sunset'] = weather_data['Today.Sunset'] = utc_str_to_local_str(forecast_seven_days[0]['astronomical']['sunset_time'])
        weather_data['Current.FireDanger'] = 'None' if not forecast_seven_days[0]['fire_danger'] else forecast_seven_days[0]['fire_danger']
        weather_data["Current.NowLabel"] = forecast_seven_days[0]['now']['now_label']
        weather_data["Current.LaterLabel"] = forecast_seven_days[0]['now']['later_label']

        # For each day of the forecast...
        for i, forecast_day in enumerate(forecast_seven_days):
            forecast_datetime = utc_str_to_local_datetime(forecast_seven_days[i]['date'])
            # The names for days - short (Mon) and long (Monday)
            set_key(weather_data, i, "ShortDay", forecast_datetime.strftime('%a'))
            set_key(weather_data, i, "Title", forecast_datetime.strftime('%A'))
            set_key(weather_data, i, "LongDay", forecast_datetime.strftime('%A'))
            # Date (Apr 4)
            set_key(weather_data, i, "ShortDate", forecast_datetime.strftime('%b ') + forecast_datetime.strftime('%d').lstrip('0'))
            # Outlook / Condition (same thing)
            set_key(weather_data, i, "Outlook", forecast_seven_days[i]['short_text'])
            set_key(weather_data, i, "Condition", forecast_seven_days[i]['short_text'])
            # Outlook / Condition (same thing) - extended text forecast.
            # For the current day, for now, add the warnings in if there are any.
            if i == 0 and warnings_text:
                extended_text_plus_warnings = f'{forecast_seven_days[i]["extended_text"]}\n\n{warnings_text}'
                set_key(weather_data, i, "OutlookLong", extended_text_plus_warnings)
                set_key(weather_data, i, "ConditionLong", extended_text_plus_warnings)
            else:
                set_key(weather_data, i, "OutlookLong", forecast_seven_days[i]['extended_text'])
                set_key(weather_data, i, "ConditionLong", forecast_seven_days[i]['extended_text'])
            # Weather icon (current day is different - we use night icons if it is night...)
            icon_code = "na"
            try:
                if i == 0 and forecast_seven_days[i]['now']['is_night']:
                    icon_code = Store.WEATHER_CODES_NIGHT[forecast_seven_days[i]['icon_descriptor']]
                else:
                    icon_code = Store.WEATHER_CODES[forecast_seven_days[i]['icon_descriptor']]
            except KeyError:
                log(f'Could not find icon code for BOM icon_descriptor: "{forecast_seven_days[i]["icon_descriptor"]}"')

            set_keys(weather_data, i, ["OutlookIcon", "ConditionIcon"], f'{icon_code}.png')
            set_keys(weather_data, i, ["FanartCode"], icon_code)
            # Maxes, Mins
            set_keys(weather_data, i, ["HighTemp", "HighTemperature"], forecast_seven_days[i]['temp_max'])
            set_keys(weather_data, i, ["LowTemp", "LowTemperature"], forecast_seven_days[i]['temp_min'])
            # Chance & amount of rain
            set_keys(weather_data, i, ["RainChance", "ChancePrecipitation"], f'{forecast_seven_days[i]["rain"]["chance"]}%')
            amount_min = forecast_seven_days[i]['rain']['amount']['min'] or '0'
            amount_max = forecast_seven_days[i]['rain']['amount']['max'] or '0'
            if amount_min == '0' and amount_max == '0':
                set_keys(weather_data, i, ["RainChanceAmount", "Precipitation"], 'None')
            else:
                set_keys(weather_data, i, ["RainChanceAmount", "Precipitation"], f'{amount_min}-{amount_max}mm')
            # UV - Predicted max, text for such, and the recommended 'Wear Sun Protection' period
            set_key(weather_data, i, 'UVIndex',  f'{forecast_seven_days[i]["uv"]["max_index"]}')
            if forecast_seven_days[i]['uv']['category']:
                set_key(weather_data, i, 'UVIndex', f'{forecast_seven_days[i]["uv"]["max_index"]} ({forecast_seven_days[i]["uv"]["category"].title()})')
                set_key(weather_data, i, 'UVCategory', forecast_seven_days[i]['uv']['category'].title())
            else:
                set_key(weather_data, i, 'UVCategory', "None")
            if forecast_seven_days[i]['uv']['start_time']:
                set_key(weather_data, i, 'UVStartProtection', utc_str_to_local_str(forecast_seven_days[i]['uv']['start_time']))
            else:
                set_key(weather_data, i, 'UVStartProtection', 'N/A')
            if forecast_seven_days[i]['uv']['end_time']:
                set_key(weather_data, i, 'UVEndProtection', utc_str_to_local_str(forecast_seven_days[i]['uv']['end_time']))
            else:
                set_key(weather_data, i, 'UVEndProtection', 'N/A')

        # Cleanup & Data massaging

        # Forecast min can be None (presumably as 'past the forecast'), so instead then use the 'temp_later' (i.e. minimum to come)
        if weather_data['Current.LowTemp'] == "None":
            set_keys(weather_data, 0, ["LowTemp", "LowTemperature"], forecast_seven_days[0]['now']['temp_later'])

        # Missing data that was available at Weatherzone but is not available from the BOM API
        weather_data['Current.DewPoint'] = "N/A"
        weather_data['Current.Pressure'] = "N/A"
        # weather_data['Current.FireDanger'] -> use only FireDanger as is now text already

    return weather_data


###########################################################
# MAIN (only for unit testing outside of Kodi)

if __name__ == "__main__":

    geohashes_to_test = ['r1r11df', 'r1f94ew']
    for geohash in geohashes_to_test:
        log(f'Getting weather data from BOM for geohash "{geohash}"')
        weather_data = bom_forecast(geohash)

        for key in sorted(weather_data):
            if weather_data[key] == "?" or weather_data[key] == "na":
                log("**** MISSING: ")
            log(f'{key}: "{weather_data[key]}"')

"""
BOM API

Information about the area the geohash represents:
https://api.weather.bom.gov.au/v1/locations/r659gg5 

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
        "response_timestamp": "2021-04-23T03:03:17Z"
    }
}

Current Observations 
https://api.weather.bom.gov.au/v1/locations/r659gg/observations

{
    "data": {
        "gust": {
            "speed_kilometre": 11, 
            "speed_knot": 6
        }, 
        "humidity": 45, 
        "rain_since_9am": 0, 
        "station": {
            "bom_id": "061425", 
            "distance": 2226, 
            "name": "Gosford"
        }, 
        "temp": 20.2, 
        "temp_feels_like": 18, 
        "wind": {
            "direction": "SSW", 
            "speed_kilometre": 9, 
            "speed_knot": 5
        }
    }, 
    "metadata": {
        "issue_time": "2021-04-23T03:11:02Z", 
        "response_timestamp": "2021-04-23T03:24:08Z"
    }
}

Weather warnings for geohash:
https://api.weather.bom.gov.au/v1/locations/rhzwe9e/warnings

{
    "data": [
        {
            "expiry_time": "2021-04-24T02:03:41.000Z", 
            "id": "QLD_RC051_IDQ20712", 
            "issue_time": "2021-04-22T23:03:41Z", 
            "phase": "final", 
            "short_title": "Flood Warning", 
            "state": "QLD", 
            "title": "Flood Warning for Russell River", 
            "type": "flood_warning", 
            "warning_group_type": "major"
        }, 
        {
            "expiry_time": "2021-04-23T09:26:45.000Z", 
            "id": "QLD_FL028_IDQ20900", 
            "issue_time": "2021-04-22T03:26:45Z", 
            "phase": "final", 
            "short_title": "Flood Watch", 
            "state": "QLD", 
            "title": "Flood Watch for Barron River", 
            "type": "flood_watch", 
            "warning_group_type": "major"
        }
    ], 
    "metadata": {
        "response_timestamp": "2021-04-23T03:07:57Z"
    }
}

7 Day Forecast
https://api.weather.bom.gov.au/v1/locations/r659gg/forecasts/daily

{
    "data": [
        {
            "astronomical": {
                "sunrise_time": "2021-04-22T20:23:29Z", 
                "sunset_time": "2021-04-23T07:24:46Z"
            }, 
            "date": "2021-04-22T14:00:00Z", 
            "extended_text": "Mostly sunny. Areas of smoke haze this morning. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "hazy", 
            "now": {
                "is_night": false, 
                "later_label": "Overnight Min", 
                "now_label": "Max", 
                "temp_later": 10, 
                "temp_now": 22
            }, 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 0
            }, 
            "short_text": "Sunny. Possible smoke haze.", 
            "temp_max": 22, 
            "temp_min": 8, 
            "uv": {
                "category": "moderate", 
                "end_time": "2021-04-23T04:00:00Z", 
                "max_index": 4, 
                "start_time": "2021-04-22T23:40:00Z"
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-23T20:24:14Z", 
                "sunset_time": "2021-04-24T07:23:40Z"
            }, 
            "date": "2021-04-23T14:00:00Z", 
            "extended_text": "Mostly sunny. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "mostly_sunny", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "short_text": "Sunny.", 
            "temp_max": 22, 
            "temp_min": 10, 
            "uv": {
                "category": "moderate", 
                "end_time": "2021-04-24T03:40:00Z", 
                "max_index": 4, 
                "start_time": "2021-04-24T00:00:00Z"
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-24T20:24:59Z", 
                "sunset_time": "2021-04-25T07:22:35Z"
            }, 
            "date": "2021-04-24T14:00:00Z", 
            "extended_text": "Mostly sunny. Medium (40%) chance of showers. Light winds becoming southerly 15 to 20 km/h during the day.", 
            "fire_danger": null, 
            "icon_descriptor": "shower", 
            "rain": {
                "amount": {
                    "max": 1, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 40
            }, 
            "short_text": "Possible shower.", 
            "temp_max": 21, 
            "temp_min": 10, 
            "uv": {
                "category": "moderate", 
                "end_time": "2021-04-25T03:50:00Z", 
                "max_index": 4, 
                "start_time": "2021-04-24T23:50:00Z"
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-25T20:25:44Z", 
                "sunset_time": "2021-04-26T07:21:31Z"
            }, 
            "date": "2021-04-25T14:00:00Z", 
            "extended_text": "Partly cloudy. Medium (40%) chance of showers. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "shower", 
            "rain": {
                "amount": {
                    "max": 1, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 40
            }, 
            "short_text": "Possible shower.", 
            "temp_max": 21, 
            "temp_min": 12, 
            "uv": {
                "category": "moderate", 
                "end_time": "2021-04-26T04:00:00Z", 
                "max_index": 5, 
                "start_time": "2021-04-25T23:40:00Z"
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-26T20:26:29Z", 
                "sunset_time": "2021-04-27T07:20:28Z"
            }, 
            "date": "2021-04-26T14:00:00Z", 
            "extended_text": "Partly cloudy. Slight (30%) chance of a shower. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "mostly_sunny", 
            "rain": {
                "amount": {
                    "max": 0.4, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 30
            }, 
            "short_text": "Partly cloudy.", 
            "temp_max": 21, 
            "temp_min": 10, 
            "uv": {
                "category": null, 
                "end_time": null, 
                "max_index": null, 
                "start_time": null
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-27T20:27:14Z", 
                "sunset_time": "2021-04-28T07:19:26Z"
            }, 
            "date": "2021-04-27T14:00:00Z", 
            "extended_text": "Partly cloudy. Slight (30%) chance of a shower. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "mostly_sunny", 
            "rain": {
                "amount": {
                    "max": 1, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 30
            }, 
            "short_text": "Partly cloudy.", 
            "temp_max": 21, 
            "temp_min": 12, 
            "uv": {
                "category": null, 
                "end_time": null, 
                "max_index": null, 
                "start_time": null
            }
        }, 
        {
            "astronomical": {
                "sunrise_time": "2021-04-28T20:27:59Z", 
                "sunset_time": "2021-04-29T07:18:25Z"
            }, 
            "date": "2021-04-28T14:00:00Z", 
            "extended_text": "Partly cloudy. Medium (40%) chance of showers. Light winds.", 
            "fire_danger": null, 
            "icon_descriptor": "shower", 
            "rain": {
                "amount": {
                    "max": 2, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 40
            }, 
            "short_text": "Possible shower.", 
            "temp_max": 21, 
            "temp_min": 11, 
            "uv": {
                "category": null, 
                "end_time": null, 
                "max_index": null, 
                "start_time": null
            }
        }
    ], 
    "metadata": {
        "forecast_region": "Central Coast", 
        "forecast_type": "metropolitan", 
        "issue_time": "2021-04-23T00:04:22Z", 
        "response_timestamp": "2021-04-23T03:06:43Z"
    }
}

3 Hourly Forecast:
https://api.weather.bom.gov.au/v1/locations/r659gg/forecasts/3-hourly

{
    "data": [
        {
            "icon_descriptor": "hazy", 
            "is_night": false, 
            "next_forecast_period": "2021-04-23T06:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 0
            }, 
            "temp": 21, 
            "time": "2021-04-23T03:00:00Z", 
            "wind": {
                "direction": "SW", 
                "speed_kilometre": 11, 
                "speed_knot": 6
            }
        }, 
        {
            "icon_descriptor": "hazy", 
            "is_night": false, 
            "next_forecast_period": "2021-04-23T09:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 0
            }, 
            "temp": 21, 
            "time": "2021-04-23T06:00:00Z", 
            "wind": {
                "direction": "SW", 
                "speed_kilometre": 9, 
                "speed_knot": 5
            }
        }, 
        {
            "icon_descriptor": "hazy", 
            "is_night": true, 
            "next_forecast_period": "2021-04-23T12:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 0
            }, 
            "temp": 17, 
            "time": "2021-04-23T09:00:00Z", 
            "wind": {
                "direction": "NNE", 
                "speed_kilometre": 4, 
                "speed_knot": 2
            }
        }, 
        {
            "icon_descriptor": "hazy", 
            "is_night": true, 
            "next_forecast_period": "2021-04-23T15:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 0
            }, 
            "temp": 15, 
            "time": "2021-04-23T12:00:00Z", 
            "wind": {
                "direction": "NW", 
                "speed_kilometre": 6, 
                "speed_knot": 3
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-23T18:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 11, 
            "time": "2021-04-23T15:00:00Z", 
            "wind": {
                "direction": "WSW", 
                "speed_kilometre": 11, 
                "speed_knot": 6
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-23T21:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 10, 
            "time": "2021-04-23T18:00:00Z", 
            "wind": {
                "direction": "W", 
                "speed_kilometre": 13, 
                "speed_knot": 7
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-24T00:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 11, 
            "time": "2021-04-23T21:00:00Z", 
            "wind": {
                "direction": "W", 
                "speed_kilometre": 13, 
                "speed_knot": 7
            }
        }, 
        {
            "icon_descriptor": "sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-24T03:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 19, 
            "time": "2021-04-24T00:00:00Z", 
            "wind": {
                "direction": "WSW", 
                "speed_kilometre": 11, 
                "speed_knot": 6
            }
        }, 
        {
            "icon_descriptor": "sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-24T06:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 22, 
            "time": "2021-04-24T03:00:00Z", 
            "wind": {
                "direction": "W", 
                "speed_kilometre": 7, 
                "speed_knot": 4
            }
        }, 
        {
            "icon_descriptor": "sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-24T09:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 21, 
            "time": "2021-04-24T06:00:00Z", 
            "wind": {
                "direction": "E", 
                "speed_kilometre": 9, 
                "speed_knot": 5
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-24T12:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 15, 
            "time": "2021-04-24T09:00:00Z", 
            "wind": {
                "direction": "NE", 
                "speed_kilometre": 6, 
                "speed_knot": 3
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-24T15:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 13, 
            "time": "2021-04-24T12:00:00Z", 
            "wind": {
                "direction": "WNW", 
                "speed_kilometre": 9, 
                "speed_knot": 5
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-24T18:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 12, 
            "time": "2021-04-24T15:00:00Z", 
            "wind": {
                "direction": "WSW", 
                "speed_kilometre": 13, 
                "speed_knot": 7
            }
        }, 
        {
            "icon_descriptor": "sunny", 
            "is_night": true, 
            "next_forecast_period": "2021-04-24T21:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 11, 
            "time": "2021-04-24T18:00:00Z", 
            "wind": {
                "direction": "WSW", 
                "speed_kilometre": 15, 
                "speed_knot": 8
            }
        }, 
        {
            "icon_descriptor": "sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-25T00:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 11, 
            "time": "2021-04-24T21:00:00Z", 
            "wind": {
                "direction": "WSW", 
                "speed_kilometre": 15, 
                "speed_knot": 8
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-25T03:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 5
            }, 
            "temp": 19, 
            "time": "2021-04-25T00:00:00Z", 
            "wind": {
                "direction": "SW", 
                "speed_kilometre": 15, 
                "speed_knot": 8
            }
        }, 
        {
            "icon_descriptor": "mostly_sunny", 
            "is_night": false, 
            "next_forecast_period": "2021-04-25T06:00:00Z", 
            "rain": {
                "amount": {
                    "max": null, 
                    "min": 0, 
                    "units": "mm"
                }, 
                "chance": 10
            }, 
            "temp": 21, 
            "time": "2021-04-25T03:00:00Z", 
            "wind": {
                "direction": "S", 
                "speed_kilometre": 15, 
                "speed_knot": 8
            }
        }
    ], 
    "metadata": {
        "issue_time": "2021-04-23T00:04:15Z", 
        "response_timestamp": "2021-04-23T03:23:14Z"
    }
}

Rain Forecast - Next 3 Hours (I think?)
https://api.weather.bom.gov.au/v1/locations/rhzwe9e/forecast/rain

{
    "data": {
        "amount": {
            "max": 1.2, 
            "min": 0.2, 
            "units": "mm"
        }, 
        "chance": 52, 
        "period": "PT3H", 
        "start_time": "2021-04-23T06:00:00Z"
    }, 
    "metadata": {
        "response_timestamp": "2021-04-23T03:27:50Z"
    }
}

"""