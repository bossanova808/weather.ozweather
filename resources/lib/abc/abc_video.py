# -*- coding: utf-8 -*-
import requests
import re
import sys
import xbmc

# Small hack to allow for unit testing - see common.py for explanation
if not xbmc.getUserAgent():
    sys.path.insert(0, '../../..')

from resources.lib.store import Store
from resources.lib.common import *


def get_abc_weather_video_link():

    try:
        r = requests.get(Store.ABC_URL)
        videos = re.findall(Store.ABC_WEATHER_VIDEO_PATTERN, r.text)

        # for video in videos:
        #     print(video)

        try:
            url = f'{Store.ABC_STUB}/{videos[1][0]}/{videos[1][1]}/{videos[1][2]}/{videos[1][3]}.mp4'
            return url
        except Exception as inst:
            log("Couldn't get ABC video URL from scraped page: " + str(inst))
            return ""

    except Exception as inst:
        log("********** Couldn't get ABC video page at all: " + str(inst))
        return ""


# UNIT TESTING
if __name__ == "__main__":
    log("\nTesting scraping of ABC Weather Video - here's the 'Best' link:\n")
    log(get_abc_weather_video_link())


# ABC VIDEO URL NOTES
# 2023
# view the source on: https://www.abc.net.au/news/weather
# search for 'mp4'
# https://mediacore-live-production.akamaized.net/video/01/im/Z/0m.mp4
# the 0m is the quality

#### LEGACY INFO:
# note date and quality level variables...
# view source on https://www.abc.net.au/news/newschannel/weather-in-90-seconds/ and find mp4 to see this list,
# the end of the URL can change regularly
# {'url': 'https://abcmedia.akamaized.net/news/news24/wins/201403/WINs_Weather1_0703_1000k.mp4', 'contentType': 'video/mp4', 'codec': 'AVC', 'bitrate': '928', 'width': '1024', 'height': '576', 'filesize': '11657344'}
# {'url': 'https://abcmedia.akamaized.net/news/news24/wins/201403/WINs_Weather1_0703_256k.mp4', 'contentType': 'video/mp4', 'codec': 'AVC', 'bitrate': '170', 'width': '320', 'height': '180', 'filesize': '2472086'}
# {'url': 'https://abcmedia.akamaized.net/news/news24/wins/201403/WINs_Weather1_0703_512k.mp4', 'contentType': 'video/mp4', 'codec': 'AVC', 'bitrate': '400', 'width': '512', 'height': '288', 'filesize': '5328218'}
# {'url': 'https://abcmedia.akamaized.net/news/news24/wins/201403/WINs_Weather1_0703_trw.mp4', 'contentType': 'video/mp4', 'codec': 'AVC', 'bitrate': '1780', 'width': '1280', 'height': '720', 'filesize': '21599356'}
# Other URLs - should match any of these
# https://abcmedia.akamaized.net/news/news24/wins/201409/WINm_Update1_0909_VSB03WF2_512k.mp4&
# https://abcmedia.akamaized.net/news/news24/wins/201409/WINs_Weather2_0209_trw.mp4
