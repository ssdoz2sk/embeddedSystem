
from pymongo import MongoClient
from django.conf import settings

def mongoClient():
    """
        MONGODB_OPTIOINS = {
            'HOST': '127.0.0.1',
            'PORT': 27017,
            'DB': 'embeddedSystem',
        }
    :return:
        Database of MongoClient
    """

    options = {}
    if hasattr(settings, 'MONGODB_OPTIOINS'):
        options = settings.MONGODB_OPTIOINS

    if not options.get('DB'):
        raise ValueError('MONGODB_OPTIONS should has options named DB')

    host = options.get('HOST', '127.0.0.1')
    port = options.get('PORT', 27017)
    db = options.get('DB')
    client = MongoClient(host, port)

    return client[db]