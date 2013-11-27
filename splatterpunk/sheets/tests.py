import logging

from django.contrib.auth import get_user_model
from django.test import TestCase

import factory

from rest_framework.renderers import JSONRenderer

from .models import Sheet
from .serializers import SheetSerializer
from .utils import logged_in


# Suppress annoying and irrelevant debug information
logging.getLogger('factory').setLevel(logging.WARNING)
logging.getLogger('south').setLevel(logging.WARNING)


# Test Utils
def jsonize(qs_or_instance, Serializer, many=False):
    serializer = Serializer(qs_or_instance, many=many)
    return JSONRenderer().render(serializer.data).decode('utf-8')


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = get_user_model()

    username = factory.Sequence(lambda n: 'person{0}'.format(n))
    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))
    first_name = "Test"
    last_name = "User"

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password(self.username)


class SheetFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Sheet

    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: 'sheet{0}'.format(n))


class ApiTest(TestCase):
    def test_sheets_list(self):
        num_sheets = 10
        SheetFactory.create_batch(num_sheets)

        self.assertEqual(Sheet.objects.count(), num_sheets)

        sheets = jsonize(Sheet.objects.all(), SheetSerializer, many=True)

        r = self.client.get('/sheets/')

        self.assertJSONEqual(sheets, r.content.decode('utf-8'))

    def test_sheet_instance(self):
        sheet = SheetFactory.create()

        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        r = self.client.get('/sheets/{id}/'.format(id=sheet.id))

        self.assertJSONEqual(json_sheet, r.content.decode('utf-8'))

    @logged_in
    def test_sheet_create(self, user):
        r = self.client.post('/sheets/', {
            "name": "Jack",
        })

        sheet = Sheet.objects.get(user=user, name="Jack")
        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        self.assertJSONEqual(r.content.decode('utf-8'), json_sheet)

    def test_bad_sheet_create(self):
        r = self.client.post('/sheets/', {
            'name': "Jack",
        })

        self.assertEqual(r.status_code, 403)


class SheetTest(TestCase):
    pass
