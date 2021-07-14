import json
import os
import sys
from flask import request , jsonify
import logging

from modules.rest import health as rest_health
from modules.rest import items as rest_items
from modules.rest import folders as rest_folders
from modules.synology import tags

import config

config.init()

config.LOGGER.info("STARTUP SYNOLOGY PHOTOS SERVICE")


@config.APP.route('/health')
def health():
    config.LOGGER.info("GET /health - received")
    result = rest_health.health(request)
    config.LOGGER.info("GET /health - result: {}".format(result['result']))
    return jsonify(result)

@config.APP.route('/tags/count')
def tags_count():
    config.LOGGER.info("GET /tags/count - received")
    result = tags.TAGS.count()
    config.LOGGER.info("GET /tags/count - result: {}".format(result['result']))
    return jsonify(result)


@config.APP.route('/tags/get_all')
def tags_get_all():
    config.LOGGER.info("GET /tags/get_all - received")
    result = tags.TAGS.get_all_tags()
    config.LOGGER.info("GET /tags/get_all - result: {}".format(result['result']))
    return jsonify(result)


@config.APP.route('/folders/get')
def folders_get():
    id = request.args.get('id')
    config.LOGGER.info("GET /folders/get - id: %s" % (id))
    result = rest_folders.sub_folders(id)
    config.LOGGER.info("GET /folders/get - result: %s" % (result['result']))
    return jsonify(result) 

@config.APP.route('/folder/items')
def folder_items():
    id = request.args.get('id')
    config.LOGGER.info("GET /folder/items - id: %s" % (id))
    result = rest_folders.items(id)
    config.LOGGER.info("GET /folder/items - result: %s" % (result['result']))
    return jsonify(result) 

@config.APP.route('/items/info')
def items_info():
    ids = request.args.get('ids')
    details=request.args.get('details')
    config.LOGGER.info("GET /items/info - ids: %s - details: %s" % (ids,details))
    result = rest_items.info(ids,details)
    config.LOGGER.info("GET /items/into - result: %s" % (result['result']))
    return jsonify(result) 

# sets item datetaken to UTC timestamp (UNIX epoch in seconds)
@config.APP.route('/item/time', methods=["PUT"])
def item_set_time():
    id = request.args.get('id')
    time = request.args.get('time')
    config.LOGGER.info("PUT /item/time - id: %s" % (id))
    result = rest_items.set_time(id,time)
    config.LOGGER.info("PUT /item/time - result: %s" % (result['result']))
    return jsonify(result) 




if __name__ == "__main__":
    from waitress import serve
    config.LOGGER.info("STARTUP waitress server on port %s ..." % (config.SYNOLOGY_REST_PORT))
    serve(config.APP, host="0.0.0.0", port=config.SYNOLOGY_REST_PORT)

