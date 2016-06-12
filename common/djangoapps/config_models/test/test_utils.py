import textwrap

from django.db import models
from django.test import TestCase
from django.utils import timezone
from django.utils.six import BytesIO

from config_models.models import ConfigurationModel
from config_models.utils import deserialize_json

from xmodule.modulestore import ModuleStoreEnum


class ExampleDeserializeConfig(ConfigurationModel):
    """
    Test model for testing deserialization of ``ConfigurationModels`` with keyed configuration.
    """
    KEY_FIELDS = ('name',)

    name = models.TextField()
    int_field = models.IntegerField(default=10)


class ConfigurationModelTests(TestCase):
    """
    Tests of ConfigurationModel
    """
    def setUp(self):
        super(ConfigurationModelTests, self).setUp()

    def test_deserialization(self):
        self.assertEquals(0, len(ExampleDeserializeConfig.objects.all()))
        start_date = timezone.now()
        test_json = textwrap.dedent("""
            {
                "model": "config_models.exampledeserializeconfig",
                "data": [
                          {
                            "name": "betty",
                            "enabled": true,
                            "int_field": 5
                           },
                          {
                            "name": "fred",
                            "enabled": false
                          }
                        ]
            }
            """)

        stream = BytesIO(test_json)
        deserialize_json(stream, ModuleStoreEnum.UserID.test)

        self.assertEquals(2, len(ExampleDeserializeConfig.objects.all()))

        betty = ExampleDeserializeConfig.current('betty')
        self.assertTrue(betty.enabled)
        self.assertEquals(5, betty.int_field)
        self.assertTrue(betty.change_date > start_date)
        self.assertEquals(ModuleStoreEnum.UserID.test, betty.changed_by.id)

        fred = ExampleDeserializeConfig.current('fred')
        self.assertFalse(fred.enabled)
        self.assertEquals(10, fred.int_field)
        self.assertTrue(fred.change_date > start_date)
        self.assertEquals(ModuleStoreEnum.UserID.test, fred.changed_by.id)


