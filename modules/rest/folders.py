from modules.synology import folders as synology_folders

def items(id):
    result = None
    if (id == None):
        result = {'result':'error - folder id not defined'}
    else:
        result = synology_folders.items(id)
    return result    

def sub_folders(id):
    result = None
    if (id == None):
        result = {'result':'error - parent folder id not defined'}
    else:
        result = synology_folders.sub_folders(id)
    return result