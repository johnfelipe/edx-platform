"""
Utilities for working with ConfigurationModels.
"""
from django.apps import apps
from rest_framework.parsers import JSONParser
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


def get_serializer_class(configuration_model):
    """ Returns a ConfigurationModel serializer class for the supplied configuration_model. """
    class AutoConfigModelSerializer(ModelSerializer):
        """Serializer class for configuration models."""

        class Meta(object):
            """Meta information for AutoConfigModelSerializer."""
            model = configuration_model

        def create(self, validated_data):
            if "changed_by_id" in self.context:
                validated_data['changed_by'], _ = User.objects.get_or_create(id=self.context["changed_by_id"])
            return super(AutoConfigModelSerializer, self).create(validated_data)

    return AutoConfigModelSerializer


def deserialize_json(stream, user_id):
    """
    Given a stream containing JSON, deserializers the JSON into ConfigurationModel instances.

    The stream is expected to be in the following format:
        { "model": "config_models.exampleconfigurationmodel",
          "data": [
                    { "enabled": True,
                      "color": "black"
                      ...
                    },
                    { "enabled": False,
                      "color": "yellow"
                      ...
                    },
                    ...
                  ]
        }

    If the provided stream does not contain valid JSON for the ConfigurationModel specified,
    an Exception will be raised.
    """
    parsed_json = JSONParser().parse(stream)
    serializer_class = get_serializer_class(apps.get_model(parsed_json["model"]))
    serializer = serializer_class(data=parsed_json["data"], context={'changed_by_id': user_id}, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        raise Exception(serializer.error_messages)
