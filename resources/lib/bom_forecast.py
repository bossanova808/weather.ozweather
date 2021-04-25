import datetime

import requests
from common import *


"""
(See bottom of this file for BOM API examples)

KODI STANDARD Weather Info Labels
(from https://kodi.wiki/view/InfoLabels#Weather_labels)

** General:
Location, 
Updated, 
WeatherProvider

** Observations / Current:
Current.Condition, 
Current.Temperature, 
Current.FeelsLike, 
Current.UVIndex, 
Current.Wind (From <wind dir.> at <speed> <unit>), 
Current.WindSpeed, 
Current.WindDirection, 
Current.DewPoint, 
Current.Humidity,

** Forecast:
Day[0-6].Title, 
Day[0-6].HighTemp, 
Day[0-6].LowTemp, 
Day[0-6].Outlook, 

OzWEATHER EXTENDED Info Labels
Current.ConditionLong - longer text for the current day's forecast
Current.WindGust

"""


def utc_str_to_local_str(utc_str: str, utc_format: str = '%Y-%m-%dT%H:%M:%SZ', local_format: str = '%I:%M %p'):
    """
    :param utc_str: UTC time string
    :param utc_format: format of UTC time string
    :param local_format: format of local time string
    :return: local time string
    """
    temp1 = datetime.datetime.strptime(utc_str, utc_format)
    temp2 = temp1.replace(tzinfo=datetime.timezone.utc)
    local_time = temp2.astimezone()
    return local_time.strftime(local_format).lstrip('0')


# Convert a fire danger numerical rating to human friendly text
# Fire danger rating may also be 'null'

def fire_danger_to_text(fire_danger_float):
    if fire_danger_float == 'null':
        return "None"
    elif 0.0 <= fire_danger_float <= 5.99:
        return "Low"
    elif 6 <= fire_danger_float <= 11.99:
        return "Moderate"
    elif 12.0 <= fire_danger_float <= 24.99:
        return "High"
    elif 25.0 <= fire_danger_float <= 49.99:
        return "Very High"
    elif 50.0 <= fire_danger_float <= 74.99:
        return "Severe"
    elif 75.0 <= fire_danger_float <= 99.99:
        return "Extreme"
    elif fire_danger_float >= 100.0:
        return "Catastrophic"
    else:
        return "?"


def bom_forecast(geohash):

    # The area hash is the geohash minus the last character
    areahash = geohash[:-1]

    bom_api_url_geohash = f'https://api.weather.bom.gov.au/v1/locations/{geohash}'
    bom_api_url_areahash = f'https://api.weather.bom.gov.au/v1/locations/{areahash}'

    bom_api_area_information_url = bom_api_url_geohash
    bom_api_warnings_url = f'{bom_api_url_geohash}/warnings'

    bom_api_current_observations_url = f'{bom_api_url_areahash}/observations'
    bom_api_forecast_seven_days_url = f'{bom_api_url_areahash}/forecasts/daily'
    bom_api_forecast_three_hourly_url = f'{bom_api_url_areahash}/forecasts/3-hourly'
    bom_api_forecast_rain = f'{bom_api_url_areahash}/forecast/rain'

    # Get the area information
    try:
        r = requests.get(bom_api_area_information_url)
        area_information = r.json()["data"]
        log(area_information)

    except Exception as inst:
        log(f'Error retrieving area information from {bom_api_area_information_url}')
        raise

    # Get current observations
    try:
        r = requests.get(bom_api_current_observations_url)
        current_observations = r.json()["data"]
        log(current_observations)

    except Exception as inst:
        log(f'Error retrieving current observations from {bom_api_current_observations_url}')
        raise

    # Get warnings
    try:
        r = requests.get(bom_api_warnings_url)
        warnings = r.json()["data"]
        log(warnings)

    except Exception as inst:
        log(f'Error retrieving warnings from {bom_api_warnings_url}')
        raise

    # Get 7 day forecast
    try:
        r = requests.get(bom_api_forecast_seven_days_url)
        forecast_seven_days = r.json()["data"]
        log(forecast_seven_days)

    except Exception as inst:
        log(f'Error retrieving seven day forecast from {bom_api_forecast_seven_days_url}')
        raise

    # Get 3 Hourly Forecast
    try:
        r = requests.get(bom_api_forecast_three_hourly_url)
        forecast_three_hourly = r.json()["data"]
        log(forecast_three_hourly)

    except Exception as inst:
        log(f'Error retrieving three hourly forecast from {bom_api_forecast_three_hourly_url}')
        raise

    # Get Rain Forecast
    try:
        r = requests.get(bom_api_forecast_rain)
        forecast_rain = r.json()["data"]
        log(forecast_rain)

    except Exception as inst:
        log(f'Error retrieving rain forecast from {bom_api_forecast_rain}')
        raise

    log('')

    # Gather the weather data into Kodi friendly labels
    weather_data = {}
    weather_data['Current.Condition'] = forecast_seven_days[0]['short_text']
    weather_data['Current.ConditionLong'] = forecast_seven_days[0]['extended_text']
    weather_data['Current.Sunrise'] = weather_data['Today.Sunrise'] = utc_str_to_local_str(forecast_seven_days[0]['astronomical']['sunrise_time'])
    weather_data['Current.Sunset'] = weather_data['Today.Sunset'] = utc_str_to_local_str(forecast_seven_days[0]['astronomical']['sunset_time'])
    weather_data['Current.Temperature'] = str(round(current_observations['temp']))
    weather_data['Current.FeelsLike'] = str(round(current_observations['temp_feels_like']))
    weather_data['Current.Humidity'] = current_observations['humidity']
    weather_data['Current.WindSpeed'] = current_observations['wind']['speed_kilometre']
    weather_data['Current.WindDirection'] = current_observations['wind']['direction']
    weather_data['Current.Wind'] = f'From {current_observations["wind"]["direction"]} at {current_observations["wind"]["speed_kilometre"]} km/h'
    weather_data['Current.WindGust'] = f'{current_observations["gust"]["speed_kilometre"]} km/h'
    weather_data['Current.FireDanger'] = '0' if forecast_seven_days[0]['fire_danger'] == 'null' else forecast_seven_days[0]['fire_danger']
    weather_data['Current.FireDangerText'] = fire_danger_to_text(forecast_seven_days[0]['fire_danger'])
    weather_data["Current.Precipitation"] = weather_data["Current.RainSince9"] = current_observations['rain_since_9am']

    # Missing data
    # weather_data['Current.DewPoint']
    # weather_data['Current.Pressure']

    log(weather_data)

###########################################################
# MAIN (only for unit testing outside of Kodi)

if __name__ == "__main__":

    geohashes_to_test = ['r1r11df', 'r1f94ew']
    for geohash in geohashes_to_test:
        log(f'Getting weather data from BOM for geohash "{geohash}"')
        bom_forecast(geohash)


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