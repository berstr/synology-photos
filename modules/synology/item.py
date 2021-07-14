
import requests
import json

import config
from modules.synology import login


def set_time(id,time):
    result = None

    PAYLOAD = {
        "api": '\"SYNO.FotoTeam.Browse.Item\"',
        "version" : "1",
        "method": '\"set\"',
        'id': '[{}]'.format(id),
        'time' : time
    }
    
    PAYLOAD = 'id=[{}]&time={}&api="SYNO.FotoTeam.Browse.Item"&method="set"&version=1'.format(id,time)

    PARAMS = {
        "_sid": login.getSid()
    }
    URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"
    print('PAYLOAD: {}'.format(json.dumps(PAYLOAD)))

    r = requests.post(url=URL, params=PARAMS, data=PAYLOAD) # data=json.dumps(PAYLOAD))
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        json_result = r.json()
        if json_result["success"] == True:
            result = {'result' : 'ok', 'id':id ,'time':time } 
        else:
            result = {'result' : 'synology photos error', 'ids':id, 'time':time,'synology' : json.dumps(json_result) }

    config.LOGGER.info("item.set_date() - result: {}".format(result))
    return result

# ids:      string with comma sperated item ids, example: "23,456,54,34567,87"
# details:  string with comma sperated parameters, example: "description,tag,exif,resolution"
#           if None, only ... will be returned
#           if 'full', then all will be returned
def info(ids, details=None):
    result = None
    additional='[]'

    if details != None:
        if details=="full":
            additional='["description","tag","exif","resolution","orientation","gps","thumbnail","address","geocoding_id","person"]'
        else:
            temp1 = details.split(',')
            temp2 = []
            for x in temp1:
                temp2.append('\"{}\"'.format(x))
            additional = '[{}]'.format(','.join(temp2))
    
    PARAMS = {
        "api": "SYNO.FotoTeam.Browse.Item",
        "version" : "1",
        "method": "get",
        'id': '[{}]'.format(ids),
        'additional':additional,
        "_sid": login.getSid()
    }
    URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"
    
    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        json_result = r.json()
        item_infos = []
        if json_result["success"] == True:
            list = json_result['data']['list']
            for item in list:
                item_infos.append({'id':item['id'],'info':item})
                result = {'result' : 'ok', 'ids':ids ,'details':details,'items':item_infos }    
        else:
            result = {'result' : 'synology photos error', 'ids':ids, 'details':details,'synology' : json.dumps(json_result) }

    if result['result'] == 'ok':
        config.LOGGER.info("item.info() - result: {}".format(result['result']))
    else:
        config.LOGGER.info("item.info() - result: {}".format(result))

    return result
 






'''
    "data": {
        "list": [
            {
                "additional": {
                    "address": {
                        "city": "Upper Bavaria",
                        "city_id": "Oberbayern",
                        "country": "Germany",
                        "country_id": "Deutschland",
                        "county": "Landkreis Ebersberg",
                        "county_id": "Landkreis Ebersberg",
                        "district": "",
                        "district_id": "",
                        "landmark": "",
                        "landmark_id": "",
                        "route": "Herzog-Rudolf-Weg",
                        "route_id": "Herzog-Rudolf-Weg",
                        "state": "Bavaria",
                        "state_id": "Bayern",
                        "town": "",
                        "town_id": "",
                        "village": "Zorneding",
                        "village_id": "Zorneding"
                    },
                    "description": "",
                    "exif": {
                        "aperture": "F1.8",
                        "camera": "iPhone X",
                        "exposure_time": "1/120 s",
                        "focal_length": "4.0 mm",
                        "iso": "25",
                        "lens": "iPhone X back dual camera 4mm f/1.8"
                    },
                    "geocoding_id": 366,
                    "gps": {
                        "latitude": 48.087902777777799,
                        "longitude": 11.839969444444399
                    },
                    "orientation": 6,
                    "orientation_original": 6,
                    "person": [],
                    "resolution": {
                        "height": 4032,
                        "width": 3024
                    },
                    "tag": [],
                    "thumbnail": {
                        "cache_key": "71807_1625110339",
                        "m": "ready",
                        "preview": "broken",
                        "sm": "ready",
                        "unit_id": 71807,
                        "xl": "ready"
                    }
                },
                "filename": "2020-01-11-1220-5100.JPG",
                "filesize": 6188299,
                "folder_id": 415,
                "id": 71807,
                "indexed_time": 1625093293422,
                "live_type": "photo",
                "owner_user_id": 0,
                "time": 1578745252,
                "type": "live"
            }
        ]
    },
    "success": true
}
'''