#!/usr/bin/python
# Copyright StrongArm Technologies, All Rights Reserved
# Mar-02-2021 beadon + adukalev : v0.1 : First release candidate

import sys
import warnings
import os
import datetime
import logging
import getopt

# Setup Logging
logging.basicConfig(filename='upload_results.log', format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding='utf-8', level=logging.DEBUG)

# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-6s: %(levelname)-5s: %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)


def uploadLogFiles():
        logging.info('Attempting to upload the file')
        
        command = 'scp adb_logs* sat_support@3.90.70.137:~/CONTENT/'
        stream = os.popen(command)
        output = stream.read()
        output.rstrip()

        logging.info("Status of upload: "+output)
        logging.info('File upload complete.')

        command = 'scp results* sat_support@3.90.70.137:~/CONTENT/'
        stream = os.popen(command)
        output = stream.read()
        output.rstrip()

        logging.info("Status of upload: "+output)


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "h","help=")
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
          usage()
          sys.exit()
    uploadLogFiles()

def usage():
    print(sys.argv[0])
    print "This script will prompt the user to upload logcat messages from utility get_logs.py"


main(sys.argv[1:])
exit()