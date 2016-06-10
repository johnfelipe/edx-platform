"""
Utilities for working with ConfigurationModels.
"""
import json
import sys

from django.utils import timezone
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer
)
from django.utils import six


# Unfortunately this is copied from https://github.com/django/django/blob/7f51876f99851fdc3fef63aecdfbcffa199c26b9/django/core/serializers/json.py#L70
# to be able a little manipulation of the JSON format....
def configuration_model_deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data representing a ConfigurationModel.
    """
    if not isinstance(stream_or_string, (bytes, six.string_types)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode('utf-8')
    try:
        objects = json.loads(stream_or_string)
        change_date = unicode(timezone.now())
        objects = convert_to_expected_format(objects, change_date)  # This is what was inserted!
        for obj in PythonDeserializer(objects, **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])


def convert_to_expected_format(objects, change_date):
    return_list = []
    model_name = objects["model"]
    data = objects["data"]
    for fields in data:
        fields[u"change_date"] = change_date
        return_list.append({u"model": model_name, u"fields": fields})

    return return_list
