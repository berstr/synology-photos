
import config

def health(request):
    config.LOGGER.info("GET /health")
    result = { 'result' : 'ok' }
    return result