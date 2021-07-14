from flask import Flask, jsonify, request
import os
import logging
from newrelic.agent import NewRelicContextFormatter
from logging.handlers import RotatingFileHandler

from modules.synology import login
from modules.synology import tags
#from modules.synology import folders


# Constants
SYNOLOGY_LOGIN_REFRESH = 600 # number of seconds
SYNOLOGY_PHOTO_TAGS_REFRESH = 600 # number of seconds


# The following variables are set through env variables
SYNOLOGY_FILESTATION_SERVICE = None  # <hostname>:<port>
SYNOLOGY_HOST = None  # <hostname>:<port>
SYNOLOGY_REST_PORT = '37083' # can be overwritten by env variable
SYNOLOGY_USERNAME = None
SYNOLOGY_PASSWORD = None


# The following variables are being set by the application at runtime:
APP = None
LOGGER = None
SYNOLOGY = None


# ==========================
# Init of variables
# ==========================

APP = Flask(__name__)

# SYNOLOGY_FILESTATION_SERVICE is the hostname (IP address) and port number where the synology-filestation runs
# Example: 192.168.178.99:8888
SYNOLOGY_FILESTATION_SERVICE=os.environ.get("SYNOLOGY_FILESTATION_SERVICE")
if (SYNOLOGY_FILESTATION_SERVICE == None):
    SYNOLOGY_FILESTATION_SERVICE='localhost:37081'

temp = os.environ.get("SYNOLOGY_REST_PORT")
if (temp != None):
    SYNOLOGY_REST_PORT=temp


def init():
    global SYNOLOGY_HOST, SYNOLOGY_USERNAME, SYNOLOGY_PASSWORD
    init_logger()
    # SYNOLOGY_HOST is the hostname (IP address) of the Synology Diskstation
    SYNOLOGY_HOST=os.environ.get("SYNOLOGY_HOST")
    if (SYNOLOGY_HOST == None):
        LOGGER.fatal('FATAL - env SYNOLOGY_HOST not defined - Exit service')
        quit()
    SYNOLOGY_USERNAME=os.environ.get("SYNOLOGY_USERNAME")
    if (SYNOLOGY_USERNAME == None):
        LOGGER.fatal('FATAL - env SYNOLOGY_USERNAME not defined - Exit service')
        quit()
    SYNOLOGY_PASSWORD=os.environ.get("SYNOLOGY_PASSWORD")
    if (SYNOLOGY_PASSWORD == None):
        LOGGER.fatal('FATAL - env SYNOLOGY_PASSWORD not defined - Exit service')
        quit()
    synology_login()
    #folders.init_folders()
    tags.init_tags()




def synology_login():
    global SYNOLOGY
    SYNOLOGY = login.synology_login()

def init_logger():
    global LOGGER
    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler('logs/synology-photos.log', maxBytes=10485760, backupCount=2) # max logfile size: 10MB
    newrelic_formatter = NewRelicContextFormatter()
    file_handler.setFormatter(newrelic_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    LOGGER = logger
