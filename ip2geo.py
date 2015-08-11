#!/usr/bin/python
# 
# Author:    Miguel Aguilar
# Project:   IP to Geo locator 
# Location:  Seattle, WA. Aug 5, 2015
# Script:    ip2geo.py
# Logs:      ./geoInfo.log
#
# Objective: This script is designed to take an IP and return a set of data related to its Geolocation.
#            As it stands right now, using hostnames always resolves to IP's to a GeoLocation close to
#            FreeGeoIP.net as it acts as the DNS resolver. Future versions of the script or new separate
#            script all together will be able to do a local DNS resolution to make sure the results are 
#            accurate regardless of from where the script is being executed. 
#
# Usage:   python ip2geo.py <IP|Hostname>
# Example: python ip2geo.py google.com
#

import sys
import time
import urllib2
import ast

def ip2geo(ip) :
    req = urllib2.Request('https://freegeoip.net/json/' + ip)
    ### Catch error exceptions when fetching the Geo Information
    try: 
        response = urllib2.urlopen(req, timeout=5)
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            print 'We failed to gather the geo data'
            print 'Reason: ', e.reason
            return ("\"Reason\" : \"%s\"" % (e.reason))
        elif hasattr(e,'code'):
            print 'The server could not fulfill the geo data request'
            print 'Error code: ', e.code
            return ("\"Error\" : \"%s\"" % (e.code))
    # response = urllib2.urlopen(req, timeout=5)
    else:
        ipInfo = response.read()
        
    return ipInfo

def printGeoInfo(geoInfo) :
    ### Convert the str response to a dict
    strResponse = geoInfo
    geoInfo = ast.literal_eval(strResponse)
    print ("\nGeolocation data:\n\r%s" % ("-" * 17))
    ### Prints all the dictionary keys with their values
    for key in geoInfo:
        print key, ": ", geoInfo[key]
    
    print ("\n\rGoogle Maps URL:   https://www.google.com/maps/@%s,%s,10z" % (geoInfo['latitude'], geoInfo['longitude']))

def saveGeoInfo(geoInfo) :
    ### Save all the information gathered to a log
    with open('geoInfo.log', 'a') as f:
        f.write(geoInfo)
        print "\n\rData appended to ./geoInfo.log"
        f.close()
        
def main() :
    ### Check to see if there are arguments
    if len(sys.argv) > 1 :
        ip = sys.argv[1]
    else :
        ip = raw_input("Enter a valid Public IP/hostname to GeoLocate: ")
    
    start = time.time()
    ### Create dict geoInfo by assigning the result of the GeoLocation request
    geoInfo = ip2geo(ip)
    
    ### Version disclaimer
    print ("\n%s" % ("*" * 36))
    print ("* ip2geo.py by Miguel Aguilar *\n\r%s" % (("*" * 36)))
    
    ### Print the GeoInfo to screen
    printGeoInfo(geoInfo)
    
    ### Save the results to ./geoInfo.log
    saveGeoInfo(geoInfo)
    
    ### Print the time elapsed since the script started
    print ("\n\rTime Elapsed: %s seconds\n\r" % (round(time.time() - start)))
    
if __name__ == "__main__" :
    main()
