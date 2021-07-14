import requests
import os
import datetime
import time
import json

import config


__SID = None
__sid_timestamp = None


def getSid():
    current_time = datetime.datetime.now()
    delta = current_time - __sid_timestamp
    if delta.total_seconds() > config.SYNOLOGY_LOGIN_REFRESH:
        synology_login()
    return __SID


def synology_login():
    global __SID
    global __sid_timestamp

    config.LOGGER.info("synology_login() - START")

    __sid_timestamp = datetime.datetime.now()
        
    result = None

    PARAMS = {
        "api": "SYNO.API.Auth",
        "version" : "3",
        "method": "login",
        "account": config.SYNOLOGY_USERNAME,
        "passwd": config.SYNOLOGY_PASSWORD,
        "session": "FileStation",
        "format": "sid"
    }
    URL = "http://" + config.SYNOLOGY_HOST + ":5000/webapi/auth.cgi"

    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        json_result = r.json()
        if json_result["success"] == True:
            __SID = json_result['data']['sid']
            config.LOGGER.info("synology_login() - filestation response - success: {} - sid: {}....".format(json_result['success'], json_result['data']['sid'][0:20]))
            result = {'result' : 'ok' }
        else:
            result = {'result' : 'synology photos error', 'synology' : json.dumps(json_result) }
            config.LOGGER.error("synology_login() - synology photos error: {}".format(json.dumps(json_result)))

    config.LOGGER.info("synology_login() - COMPLETED")
    return result
