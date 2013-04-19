# goscale/utils/json_pretty.py
"""
Add the line to settings.py::

    SERIALIZATION_MODULES = {'json-pretty': 'goscale.utils.json_pretty'}

And call dumpdata as follows::

    ./manage.py dumpdata --format=json-pretty <app_name>

"""

import codecs
import json
from django.core.serializers.json import Serializer as JSONSerializer
from django.core.serializers.json import DjangoJSONEncoder


class Serializer(JSONSerializer):
    objects = []

    def end_serialization(self):
        stream = codecs.getwriter('utf8')(self.stream)
        json.dump(self.objects, stream, cls=DjangoJSONEncoder,
                        ensure_ascii=False, **self.options)
