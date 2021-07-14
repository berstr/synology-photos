import re
from datetime import datetime, timezone

from modules.helper import parse as helper_parse
from modules.synology import item as synology_item

def set_time(id,time):
    result = None
    if (id == None):
        result = {'result':'error - item id is not defined'}
    elif (time == None):
        result = {'result':'error - new time is not defined'}
    else:
        result = synology_item.set_time(id,time)
    return result

def info(ids, details):
    result = None
    if (ids == None):
        result = {'result':'error - list of item ids not defined'}
    else:
        p='^\d+(,\d+)*$'
        m=re.match(p,ids)
        if m == None:
            result = {'result':'error - list of item ids needs to be a list of comma seperated numbers (34,564,654,87)', 'items':ids}
        else:
            item_infos = synology_item.info(ids,details)
            if item_infos['result'] == 'ok':
                __add_filename_analysis(item_infos['items'])
                __add_date_info(item_infos['items'])
                __add_time_delta(item_infos['items']) 
    return item_infos


def __add_filename_analysis(items):
    for item in items:
        item['filename_analysis'] = helper_parse.parse_filename(item['info']['filename'])

def __add_date_info(items):
    for item in items:
        item_timezone = timezone.utc
        datetime_object = datetime.fromtimestamp(item['info']['time'], item_timezone)
        item['date'] = {    'time':int(datetime_object.timestamp()), 
                            'year':datetime_object.strftime("%Y"), 
                            'month':datetime_object.strftime("%m"),
                            'day':datetime_object.strftime("%d"),
                            'hour':datetime_object.strftime("%H"),
                            'minute':datetime_object.strftime("%M"),
                            'second':datetime_object.strftime("%S"),
                            'date': datetime_object.strftime("%Y-%m-%d %H:%M:%S")
                        }


def __add_time_delta(items): # difference between date attribute (added in __add_date_info()) and the date calculated from the item filename, if the name is valid
    for item in items:
        if item['filename_analysis']['result'] == 'ok':
            if item['filename_analysis']['date'] == item['date']['date']:
                item['filename_analysis']['time_synced'] = 'true'
            else:
                item['filename_analysis']['time_synced'] = 'false'
        else:
            item['filename_analysis']['time_synced'] = 'false'


'''
sample JSON response structure:

{
            "date": {
                "date": "2021-07-12 09:47:40",
                "day": 12,
                "hour": 9,
                "minute": 47,
                "month": 7,
                "second": 40,
                "time": 1626083260,
                "year": 2021
            },
            "id": 77567,
            "info": {
                "additional": {
                    "description": "",
                    "exif": {
                        "aperture": "",
                        "camera": "",
                        "exposure_time": "",
                        "focal_length": "",
                        "iso": "",
                        "lens": ""
                    },
                    "orientation": 1,
                    "orientation_original": 1,
                    "person": [],
                    "resolution": {
                        "height": 1080,
                        "width": 1920
                    },
                    "tag": [],
                    "thumbnail": {
                        "cache_key": "77567_1626076098",
                        "m": "ready",
                        "preview": "broken",
                        "sm": "ready",
                        "unit_id": 77567,
                        "xl": "ready"
                    }
                },
                "filename": "IMG_5546.MOV",
                "filesize": 11900801,
                "folder_id": 415,
                "id": 77567,
                "indexed_time": 1626083292230,
                "owner_user_id": 0,
                "time": 1626083260,
                "type": "video"
            },
            "time_status": {
                "filename": "IMG_5546.MOV",
                "item_date": "2021-07-12 09:47:40",
                "item_time": 1626083260,
                "name_date": null,
                "name_time": null,
                "status": "false"
            },
            "valid_filename": {
                "filename": "IMG_5546.MOV",
                "result": "invalid item filename: {} - allowed: YYYY-MM-DD-hhmm-xxxx.<ext>  (with x being a number 0-9)"
            }
        }


         "geocoding_id": 1,
        "gps": {
                        "latitude": 48.1110416666667,
                        "longitude": 11.5810222222222
                    },
'''