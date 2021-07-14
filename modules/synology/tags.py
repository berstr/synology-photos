import requests
import json
import datetime
import time

import config
from modules.synology import login

TAGS = None


def init_tags():
    global TAGS
    TAGS = Tags()
    #TAGS.get_all()
    #print(TAGS.tags)

'''
def tags_count():
    result = None
    PARAMS = {
        "api": "SYNO.FotoTeam.Browse.GeneralTag",
        "version" : "1",
        "method": "count",
        "_sid": login.getSid()
    }
    URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"

    r = requests.get(url=URL, params=PARAMS)
    if r.status_code != 200:
        result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
    else:
        json_result = r.json()
        if json_result["success"] == True:
            count = json_result['data']['count']
            result = {'result' : 'ok', 'count' : count }
        else:
            result = {'result' : 'synology photos error', 'synology' : json.dumps(json_result) }
            config.LOGGER.error("tags_count() - synology photos error: {}".format(json.dumps(json_result)))

    config.LOGGER.info("tags_count() - result: {}".format(json.dumps(json_result)))
    return result

'''




class Tags:

    
    def __init__(self):
        self.time = None
        self.tags = None
        self.json_tags = None
        self.__update_instance()

    def get_all_tags(self):
        if self.__refresh():
            result = self.__update_instance()
        else:
            result = {'result' : 'ok'  , 'count': len(self.tags), 'tags' : self.json_tags }
        return result


    def count(self):
        if self.__refresh():
            result = self.__update_instance()
            if result['result'] == 'ok':
                result = {'result' : 'ok'  , 'count': len(self.tags) }
        else:
            result = {'result' : 'ok'  , 'count': len(self.tags) }
        return result


    def create(self,name):
        config.LOGGER.info("Tags.create() - name: {}".format(name))
        result = None
        exists = self.exists(name) # this will also refresh the tag list if too old
        if exists:
            result = {'result' : 'tag [{}] already exists'.format(name) }
        else:
             PARAMS = {
                "api": "SYNO.FotoTeam.Browse.GeneralTag",
                "version" : "1",
                "method": "create",
                "name": name,
                "_sid": login.getSid()
            }
        URL = "http://" + config.SYNOLOGY_HOST + "/photo/webapi/query.cgi"
        r = requests.get(url=URL, params=PARAMS)
        if r.status_code != 200:
            result = {'result' : "HTTP error - status code: {}".format(r.status_code), "http_status_code" : r.status_code}
        else:
            json_result = r.json()
            if json_result["success"] == True:
                id = json_result['data']['tag']['id']
                result = {'result' : 'ok', 'name':name, 'id':id }
                self.tags.append(Tag(id,0,name))
                
            else:
                result = {'result' : 'synology photos error', 'name':name,'synology' : json.dumps(json_result) }
        config.LOGGER.info("Tags.create() - result: {}".format(json.dumps(result)))
        return result

    def exists(self,name):
        if self.__refresh():
            self.__update_instance()
        for tag in self.tags:
            if name == tag.name:
                return True
        return False


    def __update_instance(self):
        config.LOGGER.info("Tags.__update_instance() - Start")
        self.time = datetime.datetime.now()
        result = self.__fetch_all_tags()
        if result['result'] == 'ok':
            self.json_tags = result['tags']
            self.tags=[]
            for tag in result['tags']:
                self.tags.append(Tag(tag['id'], tag['item_count'], tag['name']))
        config.LOGGER.info("Tags.__update_instance() - Completed")
        return result

    def __refresh(self):
        current_time = datetime.datetime.now()
        delta = current_time - self.time
        if delta.total_seconds() > config.SYNOLOGY_PHOTO_TAGS_REFRESH:
            return True
        else:
            return False

    def __fetch_all_tags(self):
        config.LOGGER.info("Tags.__fetch_all_tags()")
        result = None
        PARAMS = {
            "api": "SYNO.FotoTeam.Browse.GeneralTag",
            "version" : "1",
            "method": "list",
            "offset" : "0",
            "limit" : 5000, # 5000 seems to be the limit
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
                result = {'result' : 'ok'  , 'count': len(list), 'tags' : list }
            else:
                result = {'result' : 'synology photos error', 'synology' : json.dumps(json_result) }
    
        config.LOGGER.info("Tags.__fetch_all_tags() - result (partial): {} ....".format(json.dumps(result)[0:120]))
        return result


class Tag:

    def __init__(self, id, item_count, name):
        self.id = id
        self.item_count = item_count
        self.name = name
