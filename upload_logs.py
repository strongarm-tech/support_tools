#!/usr/bin/python

import sys
import warnings
import os
import datetime
import logging


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


def main():
    uploadLogFiles()


main()
exit()