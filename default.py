# -*- coding: utf-8 -*-

# *  This Program is free software; you can redistribute it and/or modify
# *  it under the terms of the GNU General Public License as published by
# *  the Free Software Foundation; either version 2, or (at your option)
# *  any later version.
# *
# *  This Program is distributed in the hope that it will be useful,
# *  but WITHOUT ANY WARRANTY; without even the implied warranty of
# *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# *  GNU General Public License for more details.
# *
# *  You should have received a copy of the GNU General Public License
# *  along with XBMC; see the file COPYING. If not, write to
# *  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
# *  http://www.gnu.org/copyleft/gpl.html
# *


import os, sys, urllib, urllib2, socket
import xbmc, xbmcvfs, xbmcgui, xbmcaddon
import re
import ftplib
import shutil
import time
import datetime
import glob

from datetime import date


# Minimal code to import bossanova808 common code
ADDON           = xbmcaddon.Addon()
CWD             = ADDON.getAddonInfo('path')
RESOURCES_PATH  = xbmc.translatePath( os.path.join( CWD, 'resources' ))
LIB_PATH        = xbmc.translatePath(os.path.join( RESOURCES_PATH, "lib" ))
sys.path.append( LIB_PATH )

from b808common import *
from weatherzone import *
from abc import *
from utilities import *

#Handy Strings
WEATHER_WINDOW  = xbmcgui.Window(12600)
WEATHERZONE_URL = 'http://www.weatherzone.com.au'
FTPSTUB = "ftp://anonymous:someone%40somewhere.com@ftp.bom.gov.au//anon/gen/radar_transparencies/"
HTTPSTUB = "http://www.bom.gov.au/products/radar_transparencies/"
RADAR_BACKGROUNDS_PATH = ""
LOOP_IMAGES_PATH = ""
TEMPUNIT = unicode(xbmc.getRegion('tempunit'), encoding='utf-8')

################################################################################
# blank out all the window properties


def clearProperties():
    log("Clearing Properties")
    try:
        setProperty(WEATHER_WINDOW, 'Weather.IsFetched',"false")
        setProperty(WEATHER_WINDOW, 'Current.IsFetched',"false")
        setProperty(WEATHER_WINDOW, 'Today.IsFetched'  ,"false")
        setProperty(WEATHER_WINDOW, 'Daily.IsFetched'  ,"false")
        setProperty(WEATHER_WINDOW, 'Radar')
        setProperty(WEATHER_WINDOW, 'Video.1')

        #now clear all the XBMC current weather properties
        setProperty(WEATHER_WINDOW, 'Current.Condition')
        setProperty(WEATHER_WINDOW, 'Current.ConditionLong')
        setProperty(WEATHER_WINDOW, 'Current.Temperature')
        setProperty(WEATHER_WINDOW, 'Current.Wind')
        setProperty(WEATHER_WINDOW, 'Current.WindDirection')
        setProperty(WEATHER_WINDOW, 'Current.WindDegree')
        setProperty(WEATHER_WINDOW, 'Current.WindGust')
        setProperty(WEATHER_WINDOW, 'Current.Pressure')
        setProperty(WEATHER_WINDOW, 'Current.FireDanger')
        setProperty(WEATHER_WINDOW, 'Current.FireDangerText')
        setProperty(WEATHER_WINDOW, 'Current.Visibility')
        setProperty(WEATHER_WINDOW, 'Current.Humidity')
        setProperty(WEATHER_WINDOW, 'Current.FeelsLike')
        setProperty(WEATHER_WINDOW, 'Current.DewPoint')
        setProperty(WEATHER_WINDOW, 'Current.UVIndex')
        setProperty(WEATHER_WINDOW, 'Current.OutlookIcon', "na.png")
        setProperty(WEATHER_WINDOW, 'Current.ConditionIcon', "na.png")
        setProperty(WEATHER_WINDOW, 'Current.FanartCode')
        setProperty(WEATHER_WINDOW, 'Current.Sunrise')
        setProperty(WEATHER_WINDOW, 'Current.Sunset')

        setProperty(WEATHER_WINDOW, 'Today.Sunrise')
        setProperty(WEATHER_WINDOW, 'Today.Sunset')
        setProperty(WEATHER_WINDOW, 'Today.moonphase')
        setProperty(WEATHER_WINDOW, 'Today.Moonphase')

        setProperty(WEATHER_WINDOW, 'Current.RainSince9')
        setProperty(WEATHER_WINDOW, 'Current.RainLastHr')
        setProperty(WEATHER_WINDOW, 'Current.Precipitation')
        setProperty(WEATHER_WINDOW, 'Current.ChancePrecipitation')
        setProperty(WEATHER_WINDOW, 'Current.SolarRadiation')


        #and all the properties for the forecast
        for count in range(0,7):
            setProperty(WEATHER_WINDOW, 'Day%i.Title'                           % count)
            setProperty(WEATHER_WINDOW, 'Day%i.RainChance'                      % count)
            setProperty(WEATHER_WINDOW, 'Day%i.RainChanceAmount'                % count)
            setProperty(WEATHER_WINDOW, 'Day%i.ChancePrecipitation'             % count)
            setProperty(WEATHER_WINDOW, 'Day%i.Precipitation'                   % count)
            setProperty(WEATHER_WINDOW, 'Day%i.HighTemp'                        % count)
            setProperty(WEATHER_WINDOW, 'Day%i.LowTemp'                         % count)
            setProperty(WEATHER_WINDOW, 'Day%i.HighTemperature'                 % count)
            setProperty(WEATHER_WINDOW, 'Day%i.LowTemperature'                  % count)
            setProperty(WEATHER_WINDOW, 'Day%i.Outlook'                         % count)
            setProperty(WEATHER_WINDOW, 'Day%i.LongOutlookDay'                  % count)
            setProperty(WEATHER_WINDOW, 'Day%i.OutlookIcon'                     % count, "na.png")
            setProperty(WEATHER_WINDOW, 'Day%i.ConditionIcon'                   % count, "na.png")
            setProperty(WEATHER_WINDOW, 'Day%i.FanartCode'                      % count)
            setProperty(WEATHER_WINDOW, 'Day%i.ShortDate'                       % count)
            setProperty(WEATHER_WINDOW, 'Day%i.ShortDay'                        % count)
            
            setProperty(WEATHER_WINDOW, 'Day.%i.ShortDate'                      % count)
            setProperty(WEATHER_WINDOW, 'Day.%i.ShortDay'                       % count)
            
            setProperty(WEATHER_WINDOW, 'Daily.%i.Title'                        % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.RainChance'                   % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.RainChanceAmount'             % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.ChancePrecipitation'          % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.Precipitation'                % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.HighTemp'                     % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.LowTemp'                      % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.HighTemperature'              % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.LowTemperature'               % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.Outlook'                      % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.LongOutlookDay'               % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.OutlookIcon'                  % count, "na.png")
            setProperty(WEATHER_WINDOW, 'Daily.%i.ConditionIcon'                % count, "na.png")
            setProperty(WEATHER_WINDOW, 'Daily.%i.FanartCode'                   % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.ShortDate'                    % count)
            setProperty(WEATHER_WINDOW, 'Daily.%i.ShortDay'                     % count)

    except Exception as inst:
        log("********** OzWeather Couldn't clear all the properties, sorry!!", inst)


################################################################################
# set the location and radar code properties

def refresh_locations():

    log("Refreshing locations from settings")
    location_set1 = ADDON.getSetting('Location1')
    location_set2 = ADDON.getSetting('Location2')
    location_set3 = ADDON.getSetting('Location3')
    locations = 0
    if location_set1 != '':
        locations += 1
        setProperty(WEATHER_WINDOW, 'Location1', location_set1)
    else:
        setProperty(WEATHER_WINDOW, 'Location1')
    if location_set2 != '':
        locations += 1
        setProperty(WEATHER_WINDOW, 'Location2', location_set2)
    else:
        setProperty(WEATHER_WINDOW, 'Location2')
    if location_set3 != '':
        locations += 1
        setProperty(WEATHER_WINDOW, 'Location3', location_set3)
    else:
        setProperty(WEATHER_WINDOW, 'Location3')

    setProperty(WEATHER_WINDOW, 'Locations', str(locations))

    log("Refreshing radar locations from settings")
    radar_set1 = ADDON.getSetting('Radar1')
    radar_set2 = ADDON.getSetting('Radar2')
    radar_set3 = ADDON.getSetting('Radar3')
    radars = 0
    if radar_set1 != '':
        radars += 1
        setProperty(WEATHER_WINDOW, 'Radar1', radar_set1)
    else:
        setProperty(WEATHER_WINDOW, 'Radar1')
    if radar_set2 != '':
        radars += 1
        setProperty(WEATHER_WINDOW, 'Radar2', radar_set2)
    else:
        setProperty(WEATHER_WINDOW, 'Radar2')
    if radar_set3 != '':
        radars += 1
        setProperty(WEATHER_WINDOW, 'Radar3', radar_set3)
    else:
        setProperty(WEATHER_WINDOW, 'Radar3')

    setProperty(WEATHER_WINDOW, 'Radars', str(locations))





################################################################################
# Downloads a radar background given a BOM radar code like IDR023 & filename
# Converts the image from indexed colour to RGBA colour

def downloadBackground(radarCode, fileName):
    
    global RADAR_BACKGROUNDS_PATH, LOOP_IMAGES_PATH

    outFileName = fileName

    #the legend file doesn't have the radar code in the filename
    if fileName == "IDR.legend.0.png":
        outFileName = "legend.png"
    else:
        #append the radar code
        fileName = radarCode + "." + fileName

    #are the backgrounds stale?
    updateRadarBackgrounds = ADDON.getSetting('BGDownloadToggle')

    if updateRadarBackgrounds:

        if xbmcvfs.exists( RADAR_BACKGROUNDS_PATH + outFileName ):
            fileCreation = os.path.getmtime( RADAR_BACKGROUNDS_PATH + outFileName)
            now = time.time()
            weekAgo = now - 7*60*60*24 # Number of seconds in a week
            #log ("filecreation: " + str(fileCreation) + " weekAgo " + str(weekAgo))
            if fileCreation < weekAgo:
                log("Backgrounds stale (older than one week) - let's refresh - " + outFileName)
                os.remove(RADAR_BACKGROUNDS_PATH + outFileName)
            else:
                log("Backgrounds not stale - use cached - " + outFileName)

    #download the backgrounds only if we don't have them yet
    if not xbmcvfs.exists( RADAR_BACKGROUNDS_PATH + outFileName ):

        log("Downloading missing background image...." + outFileName)

        #import PIL only if we need it so the add on can be run for data only
        #on platforms without PIL
        #log("Importing PIL as extra features are activated.")
        from PIL import Image
        #ok get ready to retrieve some images
        image = urllib.URLopener()

        #the legend image showing the rain scale
        try:
            imageFileIndexed = RADAR_BACKGROUNDS_PATH + "idx." + fileName
            imageFileRGB = RADAR_BACKGROUNDS_PATH + outFileName
            try:
                image.retrieve(FTPSTUB + fileName, imageFileIndexed )
            except:
                log("ftp failed, let's try http instead...")
                try:
                    image.retrieve(HTTPSTUB + fileName, imageFileIndexed )
                except:
                    log("http failed too.. sad face :( ")
                    #jump to the outer exception
                    raise
            #got here, we must have an image
            log("Downloaded background texture...now converting from indexed to RGB - " + fileName)
            im = Image.open( imageFileIndexed )
            rgbimg = im.convert('RGBA')
            rgbimg.save(imageFileRGB, "PNG")
            os.remove(imageFileIndexed)
        except Exception as inst:

            log("Error, couldn't retrieve " + fileName + " - error: ", inst)
            #ok try and get it via http instead?
            #try REALLY hard to get at least the background image
            try:
                #ok so something is wrong with image conversion - probably a PIL issue, so let's just get a minimal BG image
                if "background.png" in fileName:
                    if not '00004' in fileName:
                        image.retrieve(FTPSTUB + fileName, imageFileRGB )
                    else:
                        #national radar loop uses a different BG for some reason...
                        image.retrieve(FTPSTUB + 'IDE00035.background.png', imageFileRGB )
            except Exception as inst2:
                log("No, really, -> Error, couldn't retrieve " + fileName + " - error: ", inst2)


def prepareBackgrounds(radarCode):

    updateRadarBackgrounds = ADDON.getSetting('BGDownloadToggle')
    
    if updateRadarBackgrounds:

        log("prepareBackgrounds(%s)" % radarCode)

        downloadBackground(radarCode, "IDR.legend.0.png")
        downloadBackground(radarCode, "background.png")
        #these images don't exist for the national radar, so don't try and get them
        if radarCode != "IDR00004":
            downloadBackground(radarCode, "locations.png")
            downloadBackground(radarCode, "range.png")
            downloadBackground(radarCode, "topography.png")
            downloadBackground(radarCode, "waterways.png")


################################################################################
# Builds the radar images given a BOM radar code like IDR023
# the radar images are downloaded with each update (~60kb each time)

def buildImages(radarCode):

    global RADAR_BACKGROUNDS_PATH, LOOP_IMAGES_PATH

    #strings to store the paths we will use
    RADAR_BACKGROUNDS_PATH = xbmc.translatePath("special://profile/addon_data/weather.ozweather/radarbackgrounds/" + radarCode + "/");
    LOOP_IMAGES_PATH = xbmc.translatePath("special://profile/addon_data/weather.ozweather/currentloop/" + radarCode + "/");

    log("buildImages(%s)" % radarCode)
    log("Overlay loop path: " + LOOP_IMAGES_PATH)
    log("Backgrounds path: " + RADAR_BACKGROUNDS_PATH)

    # remove the temporary files - we only want fresh radar files
    # this results in maybe ~60k used per update.

    log("Deleting any radar overlays older than 2 hours")
    currentFiles = glob.glob (LOOP_IMAGES_PATH + "/*.png")
    for file in currentFiles:
        filetime = os.path.getmtime(file) 
        twoHoursAgo = time.time() - (2 * 60 * 60)
        if filetime < twoHoursAgo:
            log("Deleted " + str(file))
            os.remove(file)


    # if os.path.exists( LOOP_IMAGES_PATH ):
    #     log("os.path Removing previous radar files")
    #     shutil.rmtree( LOOP_IMAGES_PATH , ignore_errors=True)

    # We need make the directories to store stuff if they don't exist
    # delay hack is here to make sure OS has actually released the handle
    # from the rmtree call above before we try and make the directory

    if not os.path.exists( RADAR_BACKGROUNDS_PATH ):
        attempts = 0
        success = False
        while not success and (attempts < 20):
            try:
                os.makedirs( RADAR_BACKGROUNDS_PATH )
                success = True
                log("Successfully created " + RADAR_BACKGROUNDS_PATH)
            except:
                attempts += 1
                time.sleep(0.1)
        if not success:
            log("ERROR: Failed to create directory for radar background images!")
            return    

    if not os.path.exists( LOOP_IMAGES_PATH ):
        attempts = 0
        success = False
        while not success and (attempts < 20):
            try:
                os.makedirs( LOOP_IMAGES_PATH )
                success = True
                log("Successfully created " + LOOP_IMAGES_PATH)
            except:
                attempts += 1
                time.sleep(0.1)
        if not success:
            log("ERROR: Failed to create directory for loop images!")
            return

    prepareBackgrounds(radarCode)

    # Ok so we have the backgrounds...now it is time get the loop
    # first we retrieve a list of the available files via ftp
    # ok get ready to retrieve some images

    log("Download the radar loop")
    files = []

    log("Log in to BOM FTP")
    ftp = ftplib.FTP("ftp.bom.gov.au")
    ftp.login("anonymous", "anonymous@anonymous.org")
    ftp.cwd("/anon/gen/radar/")

    log("Get files list")
    #connected, so let's get the list
    try:
        files = ftp.nlst()
    except ftplib.error_perm, resp:
        if str(resp) == "550 No files found":
            log("No files in BOM ftp directory!")
        else:
            log("Something wrong in the ftp bit of radar images")

    log("Download the files...")
    #ok now we need just the matching radar files...
    loopPicNames = []
    for f in files:
        if radarCode in f:
            loopPicNames.append(f)

    #download the actual images, might as well get the longest loop they have
    for f in loopPicNames:
        # don't re-download ones we already have
        if not os.path.isfile(LOOP_IMAGES_PATH + "/" + f):
            #ignore the composite gif...
            if f[-3:] == "png":
                imageToRetrieve = "ftp://anonymous:someone%40somewhere.com@ftp.bom.gov.au//anon/gen/radar/" + f
                log("Retrieving new radar image: " + imageToRetrieve)
                try:
                    radarImage = urllib2.urlopen(imageToRetrieve)
                    fh = open( LOOP_IMAGES_PATH + "/" + f , "wb")
                    fh.write(radarImage.read())
                    fh.close()
                except Exception as inst:
                    log("Failed to retrieve radar image: " + imageToRetrieve + ", oh well never mind!", inst )
        else:
            log("Using cached radar image: " + f)



################################################################################
# The main forecast retrieval function
# Does either a basic forecast or a more extended forecast with radar etc.
# if the appropriate setting is set

def forecast(urlPath, radarCode):

    extendedFeatures = ADDON.getSetting('ExtendedFeaturesToggle')

    log("Getting weather from [%s] with radar [%s], extended features is: [%s]" % (urlPath, radarCode, str(extendedFeatures)))

    # Get all the weather & forecast data from weatherzone
    log("Get the forecast data from http://weatherzone.com.au" + urlPath)
    weatherData = getWeatherData(urlPath,extendedFeatures)
    for key, value in weatherData.iteritems():
        setProperty(WEATHER_WINDOW, key, value)

    # Get the ABC video link
    if extendedFeatures == "true":
        log("Get the ABC weather video link")
        url = getABCWeatherVideoLink(ADDON.getSetting("ABCQuality"))
        if url:
            setProperty(WEATHER_WINDOW, 'Video.1',url)

    # Get the radar images 
    if extendedFeatures == "true":
        log("Getting radar images for " + radarCode)
        buildImages(radarCode)
        setProperty(WEATHER_WINDOW, 'Radar', radarCode)

    # And announce everything is fetched..    
    setProperty(WEATHER_WINDOW, "Weather.IsFetched", "true")
    setProperty(WEATHER_WINDOW, 'Forecast.Updated', time.strftime("%d/%m/%Y %H:%M"))
    setProperty(WEATHER_WINDOW, 'Today.IsFetched', "true")        



################################################################################
### NOW ACTUALLTY RUN THIS PUPPY - this is main() in the old language...

# TWO MAJOR MODES - SETTINGS and FORECAST RETRIEVAL

footprints()

socket.setdefaulttimeout(100)

# SETTINGS
# the addon is being called from the settings section where the user enters their postcodes
if sys.argv[1].startswith('Location'):
    
    keyboard = xbmc.Keyboard('', LANGUAGE(32195), False)
    keyboard.doModal()
    
    if (keyboard.isConfirmed() and keyboard.getText() != ''):
        text = keyboard.getText()

        log("Doing locations search for " + text)
        locations, locationURLPaths = getLocationsForPostcodeOrSuburb(text)

        # Now get them to choose an actual location
        dialog = xbmcgui.Dialog()
        if locations != []:
            selected = dialog.select(xbmc.getLocalizedString(396), locations)
            if selected != -1:
                ADDON.setSetting(sys.argv[1], locations[selected])
                ADDON.setSetting(sys.argv[1] + 'UrlPath', locationURLPaths[selected])
        # Or indicate we did not receieve any locations
        else:
            dialog.ok(ADDONNAME, xbmc.getLocalizedString(284))


# FORECAST
# script is being called in general use, not from the settings page
# sys.argv[1] has the current location number, so get the currently selected location and grab it's forecast
else:

    # Nice neat updates - clear out everything first...
    clearProperties()

    # Set basic properties/brand
    setProperty(WEATHER_WINDOW, 'WeatherProviderLogo'       , xbmc.translatePath(os.path.join(CWD, 'resources', 'banner.png')))
    setProperty(WEATHER_WINDOW, 'WeatherProvider'           , 'Bureau of Meteorology Australia (via WeatherZone)')
    setProperty(WEATHER_WINDOW, 'WeatherVersion'            , ADDONNAME + "-" + VERSION)
    
    # Set what we updated and when
    setProperty(WEATHER_WINDOW, 'Location'              , ADDON.getSetting('Location%s' % sys.argv[1]))
    setProperty(WEATHER_WINDOW, 'Updated'               , time.strftime("%d/%m/%Y %H:%M"))
    setProperty(WEATHER_WINDOW, 'Current.Location'      , ADDON.getSetting('Location%s' % sys.argv[1]))
    setProperty(WEATHER_WINDOW, 'Forecast.City'         , ADDON.getSetting('Location%s' % sys.argv[1]))
    setProperty(WEATHER_WINDOW, 'Forecast.Country'      , "Australia")
    setProperty(WEATHER_WINDOW, 'Forecast.Updated'      , time.strftime("%d/%m/%Y %H:%M"))

    # Retrieve the currently chosen location & radar
    locationUrlPath = ""
    locationUrlPath = ADDON.getSetting('Location%sUrlPath' % sys.argv[1])
    radar = ""
    radar = ADDON.getSetting('Radar%s' % sys.argv[1])
    # If we don't have a radar code, get the national radar by default
    if radar == "":
        log("Radar code empty for location " + location +" so using default radar code IDR00004 (national radar)")
        radar = "IDR00004"
    
    # Now scrape the weather data & radar images
    forecast(locationUrlPath, radar)

# Refresh the locations
refresh_locations()

# and close out...
footprints(startup=False)
