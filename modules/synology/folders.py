import requests
import json
# from datetime import datetime, timezone

import config
from modules.synology import login
from modules.rest import items as rest_items


def sub_folders(id):
    result = None
    folders = []
    PARAMS = {
        "api": "SYNO.FotoTeam.Browse.Folder",
        "version" : "1",
        "method": "list",
        'id': id,
        "sort_direction": 'asc',
        "offset": '0',
        "limit": "2000",
        "_sid": login.getSid()
    }
    URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"

    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        json_result = r.json()
        if json_result["success"] == True:
            list = json_result['data']['list']
            for folder in list:
                folders.append({'name':folder['name'],'id':folder['id'],'parent':folder['parent']})
            result = {'result' : 'ok', 'id':id ,'folders':folders }    
        else:
            result = {'result' : 'synology photos error', 'id':id,'synology' : json.dumps(json_result) }
        
    config.LOGGER.info("folders.get() - result: {}".format(result['result']))
    return result
 

def items(id):
    result = None
    items = []
    PARAMS = {
        "api": "SYNO.FotoTeam.Browse.Item",
        "version" : "1",
        "method": "list",
        'folder_id': id,
        'additional' : '["gps","description"]',
        "sort_direction": 'asc',
        'sort_by': "takentime",
        "offset": '0',
        "limit": "2000",
        "_sid": login.getSid()
    }

    URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"

    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        # sample response:  "data": { "list": [ { "filename": "a.avi", "filesize": 734255104, "folder_id": 415, "id": 71809, 
        #                                         "indexed_time": 1625093293643, "owner_user_id": 0, "time": 1312217182, "type": "video" } , ... } ] , "success": true }
        json_result = r.json()
        if json_result["success"] == True:
            list = json_result['data']['list']
            ids =[]
            for item in list:
                ids.append(str(item['id']))
            ids_string = ','.join(ids)
            item_details = rest_items.info(ids_string,'full')
            result = {'result' : 'ok', 'id':id ,'items':item_details['items'] }    
        else:
            result = {'result' : 'synology photos error', 'id':id,'synology' : json.dumps(json_result) }
        
    config.LOGGER.info("folders.items() - result: {}".format(result['result']))
    return result
