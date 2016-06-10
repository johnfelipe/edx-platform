from django.db import models
from django.test import TestCase
from django.utils import timezone


from config_models.models import ConfigurationModel
from config_models.utils import configuration_model_deserializer


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
        test_json = ('{'
                     '  "model": "config_models.exampledeserializeconfig",'
                     '  "data": ['
                     '     {'
                     '       "name": "betty", '
                     '       "enabled": true,'
                     '       "int_field": 5'
                     '     },'
                     '     {'
                     '       "name": "fred",'
                     '       "enabled": false'
                     '     }'
                     '   ]'
                     '}'
                     )

        for obj in configuration_model_deserializer(test_json):
            obj.save()

        self.assertEquals(2, len(ExampleDeserializeConfig.objects.all()))

        betty = ExampleDeserializeConfig.current('betty')
        self.assertTrue(betty.enabled)
        self.assertEquals(5, betty.int_field)
        self.assertTrue(betty.change_date > start_date)
        self.assertIsNone(betty.changed_by)

        fred = ExampleDeserializeConfig.current('fred')
        self.assertFalse(fred.enabled)
        self.assertEquals(10, fred.int_field)
        self.assertTrue(fred.change_date > start_date)
        self.assertIsNone(fred.changed_by)


