import logging
import json

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
        """GET /sheets/ should list all sheets in the DB.
        """
        num_sheets = 10
        SheetFactory.create_batch(num_sheets)

        self.assertEqual(Sheet.objects.count(), num_sheets)

        sheets = jsonize(Sheet.objects.all(), SheetSerializer, many=True)

        r = self.client.get('/sheets/')

        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(sheets, r.content.decode('utf-8'))

    def test_sheet_instance(self):
        """GET /sheets/:id/ should show just that instance.
        """
        sheet = SheetFactory.create()
        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        r = self.client.get('/sheets/{id}/'.format(id=sheet.id))

        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(json_sheet, r.content.decode('utf-8'))

    @logged_in(UserFactory)
    def test_sheet_create(self, user):
        """POST /sheets/ with data should create a sheet, if authenticated.
        """
        r = self.client.post('/sheets/', {
            "name": "Jack",
        })

        sheet = Sheet.objects.get(user=user, name="Jack")
        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        self.assertEqual(r.status_code, 201)
        self.assertJSONEqual(r.content.decode('utf-8'), json_sheet)

    def test_bad_sheet_create(self):
        """POST /sheets/ should fail if not authenticated.
        """
        r = self.client.post('/sheets/', {
            'name': "Jack",
        })

        self.assertEqual(r.status_code, 403)

    @logged_in(UserFactory)
    def test_sheet_update(self, user):
        """PUT /sheets/:id/ should work if authenticated as the right user.
        """
        sheet = SheetFactory(user=user)
        old_name = sheet.name
        new_name = "Jack"

        r = self.client.put('/sheets/{id}/'.format(id=sheet.id), json.dumps({
            "name": new_name
        }), content_type="application/json")

        sheet = Sheet.objects.get(id=sheet.id)
        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        self.assertEqual(r.status_code, 200)
        self.assertJSONEqual(r.content.decode('utf-8'), json_sheet)
        self.assertNotEqual(old_name, new_name)

    @logged_in(UserFactory)
    def test_bad_sheet_update(self, user):
        other_user = UserFactory()
        sheet = SheetFactory(user=other_user)

        old_name = sheet.name
        new_name = "Jack"

        r = self.client.put('/sheets/{id}/'.format(id=sheet.id), json.dumps({
            "name": new_name
        }), content_type="application/json")

        sheet = Sheet.objects.get(id=sheet.id)

        self.assertEqual(r.status_code, 403)
        self.assertEqual(sheet.name, old_name)


class SheetTest(TestCase):
    pass
