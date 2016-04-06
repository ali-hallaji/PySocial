""" SESSION_SERIALIZER = 'core.json_utils.MongoJSONSerializer' """

from bson import json_util
from bson.objectid import ObjectId
from django.core.serializers.json import DjangoJSONEncoder
from django.http.response import JsonResponse


class MongoJSONEncoder(DjangoJSONEncoder):
    """
    DjangoJSONEncoder subclass that knows how to encode mongo codes
    """

    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return super(MongoJSONEncoder, self).default(o)


class MongoJSONSerializer(object):
    def dumps(self, obj):
        return json_util.dumps(
            obj,
            separators=(',', ':'),
            cls=MongoJSONEncoder
        ).encode('latin-1')

    def loads(self, data):
        return json_util.loads(data.decode('latin-1'))


class MongoJsonResponse(JsonResponse):
    def __init__(self, *args, **kwargs):
        kwargs['encoder'] = MongoJSONEncoder
        super(MongoJsonResponse, self).__init__(*args, **kwargs)
