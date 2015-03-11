# STANDARD LIB
import json

# LIBRARIES
from django.http import HttpResponse


class JsonResponse(HttpResponse):

    def __init__(self, data, **kwargs):
        if not isinstance(data, basestring):
            data = json.dumps(data)
        kwargs["content_type"] = "application/json;charset=utf8"
        return super(JsonResponse, self).__init__(data, **kwargs)
