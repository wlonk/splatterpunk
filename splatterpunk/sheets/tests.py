import logging

from django.test import TestCase

import factory

from rest_framework.renderers import JSONRenderer

from .models import Sheet
from .views import SheetView


# Suppress annoying and irrelevant debug information
logging.getLogger('factory').setLevel(logging.WARNING)
logging.getLogger('south').setLevel(logging.WARNING)


def jsonize_with_rest_framework_serializer(qs, for_view):
    Serializer = for_view().get_serializer_class()
    serializer = Serializer(qs, many=True)
    return JSONRenderer().render(serializer.data).decode('utf-8')


class SheetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sheet


class ApiTest(TestCase):
    def test_sheets(self):
        num_sheets = 10
        SheetFactory.create_batch(num_sheets)

        self.assertEqual(Sheet.objects.count(), num_sheets)

        sheets = jsonize_with_rest_framework_serializer(
            Sheet.objects.all(),
            SheetView
        )

        r = self.client.get('/sheets/')

        self.assertJSONEqual(sheets, r.content.decode('utf-8'))
