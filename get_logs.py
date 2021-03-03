#!/usr/bin/python
# Copyright StrongArm Technologies, All Rights Reserved
# Feb-27-2021 beadon + adukalev : First draft
# Mar-02-2021 beadon + adukalev : v0.1 : First release candidate

import sys
import warnings
import os
from datetime import datetime
import logging
import socket
import signal

config = { 
    'tablet' : 'HA0ZY1ZH',
    'destination_port' : 5555,
    'socket_timeout' : 5
    }

DATE_TIME = date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Setup Logging
logging.basicConfig(filename='results_'+DATE_TIME+'.log', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-6s: %(levelname)-5s: %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)

# Check if there is a tablet connected
def tabletConnected():
    try:  
        stream = os.popen('adb devices')
        output = stream.read()
        output.rstrip()
        lhs = output.split()[4]
        tablet = ''
    except Exception as e:
        logging.info("Connection to tablet not stable in the USB port. Please wait 5 seconds and try again. If this continues, please call support. Exception: " + str(e))
        logging.debug("Captured output:'" + output+ "'")
        exit()

    if  lhs == config['tablet']:
        logging.info("Detected tablet:'" + lhs + "'")
        tablet = lhs
        return tablet
        
    else:
        logging.info("Cannot detect the configured tablet for this session.  Please contact support.")
        logging.info("Detected :'" + lhs + "'")
        exit()

def setTabletDebug(tablet, port):
    # run the command to set the tablet into debugging mode
    logging.info("Attempting to set tablet '"+tablet+"' into tcpip mode")
    command = "adb tcpip " + str(port) 
    stream = os.popen(command)
    output = stream.read()
    output.rstrip()
    logging.debug("Results of '"+tablet+"' set as tcpip mode '" + output + "'") 
    # if already set, then the results will be an empty line, or 'starting in TCP mode port: 5555'

    # verify that the messages are OK, starting can be starting or restarting
    checkstring = "starting in TCP mode port: "+ str(port)
    if ( checkstring in output ) or ( '' == output ):
        logging.info("Tablet '"+tablet+"' set correctly into tcpip mode")
    else:
        logging.info("Tablet '"+tablet+"' NOT set into tcpip mode. Call Support.")
        logging.debug("Response from adb:'"+ output +"'")
        exit()

    # instruct the user to disconnect the tablet
    logging.info("Please disconnect the tablet from USB connected to the computer")
    return

def getTabletIP():
    # instruct the user to enter the tablet IP address
    logging.info("Using the TABLET now, do the following steps:")
    logging.info("Android 'Settings' Application -> 'System' -> 'About Tablet' -> 'Status'")
    logging.info("Enter the IP address seen for the wired ethernet interface in the form : 123.456.789.012")

    destination = ''
    while True:
        inp = raw_input('')
        logging.info("Entered by user: '" + inp + "'")

        # Validate the 4 part IP address is valid
        try:
            socket.inet_aton(inp)
            destination = inp
            break
        except socket.error:
            logging.info("This is an invalid IP address. Please check this and enter it again. Press Ctrl+C to exit")
    return destination

def testEndpoint( host, port ):
    # Test that the tablet is available from this laptop
    logging.info("Attempting to connect to:'"+host+"' on port:'"+str(port)+"'")
    logging.debug("Setting up the socket") 
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(config['socket_timeout'])

    location = ( host , port )
    result_of_check = a_socket.connect_ex(location)
    a_socket.close()

    if result_of_check == 0:
        logging.debug(host+":"+str(port)+" is open.")
        return True
    else:
        logging.debug(host+":"+str(port)+" is closed (or timed out)")
        return False

def beginLogging ( host, port ):
    logging.info("Logging starting for:"+host+":"+str(port)+'"')
    output = ''
    try:
        command = 'adb logcat >> adb_logs'+DATE_TIME+'.log'
        stream = os.popen(command)
        output = stream.read()
        output.rstrip()

    except KeyboardInterrupt:
        logging.info("Capture stopped.")
        logging.debug("Captured output:'" + output)
   
    logging.info("Logging ending for:"+host+":"+str(port)+'"')
    return

# prompt user to press Ctrl+C to stop the capture

## Stretch
# send the log somewhere(?)

def main():
    logging.info('Started')
    tablet = tabletConnected();  # dirty, pull the exit logic into main
    setTabletDebug(tablet, config['destination_port'])
    host = getTabletIP()
    if not testEndpoint( host, config['destination_port']) :
        logging.info("Exiting.")
    else:
        beginLogging( host, config['destination_port'])

    exit()    
main()
