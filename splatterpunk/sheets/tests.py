import logging

from django.test import TestCase

import factory

from rest_framework.renderers import JSONRenderer

from .models import Sheet
from .serializers import SheetSerializer


# Suppress annoying and irrelevant debug information
logging.getLogger('factory').setLevel(logging.WARNING)
logging.getLogger('south').setLevel(logging.WARNING)


def jsonize(qs_or_instance, Serializer, many=False):
    serializer = Serializer(qs_or_instance, many=many)
    return JSONRenderer().render(serializer.data).decode('utf-8')


class SheetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sheet


class ApiTest(TestCase):
    def test_sheets_list(self):
        num_sheets = 10
        SheetFactory.create_batch(num_sheets)

        self.assertEqual(Sheet.objects.count(), num_sheets)

        sheets = jsonize(
            Sheet.objects.all(),
            SheetSerializer,
            many=True
        )

        r = self.client.get('/sheets/')

        self.assertJSONEqual(sheets, r.content.decode('utf-8'))

    def test_sheet_instance(self):
        sheet = SheetFactory.create()

        json_sheet = jsonize(
            sheet,
            SheetSerializer,
            many=False
        )

        r = self.client.get('/sheets/{id}/'.format(id=sheet.id))

        self.assertJSONEqual(json_sheet, r.content.decode('utf-8'))
