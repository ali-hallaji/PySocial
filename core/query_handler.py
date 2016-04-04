from pymongo import MongoClient

from pysocial import settings
from class_singleton import Singleton


@Singleton
class MongoConnection(object):
    __db = None

    @classmethod
    def get_connection(cls):
        """Singleton method for running Mongo instance"""
        if cls.__db is None:
            cls.__db = MongoClient(
                settings.MONGO_DB_URL,
                serverSelectionTimeoutMS=6000, maxPoolSize=None
            )
        return cls.__db

    def __init__(self):
        self.get_connection()

    def getCursor(self, db):
        return self.__db[db]


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


