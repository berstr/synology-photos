
'''
http://192.168.178.200/photo/webapi/query.cgi?_sid=KrOpQn9noFAHSmdNg3f0UDRcbkhJlZqeS8EKJsEx9nslvcayUH_IQt9MGbQeaXmz8vF492_dlgOAGA2UGoMeY0

POST

Payload, raw text: 

id=[71807]&time=1625507609&api="SYNO.FotoTeam.Browse.Item"&method="set"&version=1


id=[71807]&
time=1578831652&
api="SYNO.FotoTeam.Browse.Item"&
method="set"&
version=1


{
    "data": {
        "error_list": []
    },
    "success": true
}


  def set_date(sname):
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

        '''
