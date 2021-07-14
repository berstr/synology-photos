
from modules.synology import tags

def tags_count():
    result = tags.tags_count()
    return result

def tags_get_all():
    result = tags.tags_get_all()
    return result    