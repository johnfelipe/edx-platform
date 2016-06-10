"""
Management commands for updating XBlockConfiguration information.
"""
from django.core.management.base import BaseCommand

from django.core import serializers
from xblock_django.models import (
    XBlockDisableConfig, XBlockConfiguration, XBlockStudioConfiguration, XBlockStudioConfigurationFlag
)
from datetime import datetime
from django.core.serializers.base import DeserializationError
from django.core.serializers.python import (
    Deserializer as PythonDeserializer, Serializer as PythonSerializer,
)
from django.utils import six
import json

class Command(BaseCommand):
    """
    This command will...
    """
    args = ''
    help = 'Creates the indexes for ContentStore and ModuleStore databases'

    def handle(self, *args, **options):

        data = serializers.serialize("json", XBlockStudioConfiguration.objects.all())

        serializer = serializers.get_serializer("json")()

        # with open("config.json", "w") as out:
        #     serializer.serialize(XBlockStudioConfiguration.objects.all(), stream=out)


        with open("update.json", "r") as out:
            #for obj in serializers.deserialize("json", out):
            for obj in Deserializer(out):
                obj.object.change_date = datetime.now()
                obj.save()


        print 'Finished command'



def Deserializer(stream_or_string, **options):
    """
    Deserialize a stream or string of JSON data.
    """
    if not isinstance(stream_or_string, (bytes, six.string_types)):
        stream_or_string = stream_or_string.read()
    if isinstance(stream_or_string, bytes):
        stream_or_string = stream_or_string.decode('utf-8')
    try:
        objects = json.loads(stream_or_string)
        objects = convert_to_expected_format(objects)
        for obj in PythonDeserializer(objects, **options):
            yield obj
    except GeneratorExit:
        raise
    except Exception as e:
        # Map to deserializer error
        six.reraise(DeserializationError, DeserializationError(e), sys.exc_info()[2])


def convert_to_expected_format(objects):
    return_list = []
    model_name = objects["model"]
    data = objects["data"]
    for fields in data:
        return_list.append({"model": model_name, "fields": fields})

    return return_list
