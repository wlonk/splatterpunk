import logging
import json

from django.contrib.auth import get_user_model
from django.test import TestCase

import factory

from rest_framework.renderers import JSONRenderer

from .models import (
    Sheet,
    BasicField,
    PointsField,
    HealthField,
)
from .serializers import (
    SheetSerializer,
    UserSerializer,
)
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


class BasicFieldFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = BasicField

    sheet = factory.SubFactory(SheetFactory)
    key = "Stat"
    max = 5
    value = 0


class PointsFieldFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = PointsField

    sheet = factory.SubFactory(SheetFactory)
    key = "Willpower"
    max = 10
    value = 5
    points = 0


class HealthFieldFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = HealthField

    sheet = factory.SubFactory(SheetFactory)
    key = "Health"
    max = 7
    bashing = 0
    lethal = 0
    aggravated = 0


class ApiTest(TestCase):
    def test_dont_reveal_private_user_data(self):
        """Serialized users shouldn't show their password hashes.
        """
        user = UserFactory()
        json_user = jsonize(user, UserSerializer)
        private_fields = (
            'date_joined',
            'groups',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'password',
            'user_permissions',
        )
        for key in private_fields:
            self.assertNotIn(key, json.loads(json_user).keys())

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

        self.assertEqual(r.status_code, 201, msg=r.content)

        sheet = Sheet.objects.get(user=user, name="Jack")
        json_sheet = jsonize(sheet, SheetSerializer, many=False)

        self.assertJSONEqual(r.content.decode('utf-8'), json_sheet)

    @logged_in(UserFactory)
    def test_sheet_create_bad_data(self, user):
        """POST /sheets/ with bad data should not create a sheet.
        """
        r = self.client.post('/sheets/', {
            "name": "Jack",
            "template": "there is no template named this"
        })

        self.assertEqual(r.status_code, 400)
        self.assertRaises(
            Sheet.DoesNotExist,
            lambda: Sheet.objects.get(user=user, name="Jack")
        )

    def test_bad_sheet_create(self):
        """POST /sheets/ should fail if not authenticated.
        """
        r = self.client.post('/sheets/', {
            'name': "Jack",
        })

        self.assertEqual(r.status_code, 403)
        self.assertRaises(
            Sheet.DoesNotExist,
            lambda: Sheet.objects.get(name="Jack")
        )

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
        """PUT /sheets/:id/ should fail if authenticated as the wrong user.
        """
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

    @logged_in(UserFactory)
    def test_sheet_delete(self, user):
        """DELETE /sheets/:id/ should remove the sheet.
        """
        sheet = SheetFactory(user=user)

        r = self.client.delete('/sheets/{id}/'.format(id=sheet.id))

        self.assertEqual(r.status_code, 204)
        self.assertRaises(
            Sheet.DoesNotExist,
            lambda: Sheet.objects.get(id=sheet.id)
        )

    @logged_in(UserFactory)
    def test_bad_sheet_delete(self, user):
        """DELETE /sheets/:id/ should fail if authenticated as the wrong user.
        """
        other_user = UserFactory()
        sheet = SheetFactory(user=other_user)

        r = self.client.delete('/sheets/{id}/'.format(id=sheet.id))

        self.assertEqual(r.status_code, 403)
        self.assertIsInstance(Sheet.objects.get(id=sheet.id), Sheet)


class SheetTest(TestCase):
    def test_health_field(self):
        """Bashing, lethal and aggravated should never exceed max.
        """
        health_field = HealthFieldFactory()
        max = health_field.max

        health_field.add_bashing(max)
        self.assertEqual(health_field.bashing, max)

        health_field.add_lethal(max)
        self.assertEqual(health_field.bashing, 0)
        self.assertEqual(health_field.lethal, max)

        health_field.add_aggravated(max)
        self.assertEqual(health_field.bashing, 0)
        self.assertEqual(health_field.lethal, 0)
        self.assertEqual(health_field.aggravated, max)

        health_field.add_aggravated(max + 1)
        self.assertEqual(health_field.aggravated, max)

    def test_points_field(self):
        """Value shouldn't exceed max, points shouldn't exceed value.
        """
        points_field = PointsFieldFactory()
        max = points_field.max
        value = points_field.value

        points_field.points = value + 1
        points_field.save()
        # @todo: Ugly. Why do we have to do this to refresh field values? I
        # guess we don't want to thrash the DB on every attribute access, but
        # still.
        points_field = PointsField.objects.get(id=points_field.id)
        self.assertEqual(points_field.points, value)

        points_field.value = max + 1
        points_field.save()
        # @todo: Ugly. Why do we have to do this to refresh field values? I
        # guess we don't want to thrash the DB on every attribute access, but
        # still.
        points_field = PointsField.objects.get(id=points_field.id)
        self.assertEqual(points_field.value, max)

    def test_basic_field(self):
        """Value shouldn't exceed max.
        """
        basic_field = BasicFieldFactory()
        max = basic_field.max

        basic_field.value = max + 1
        basic_field.save()
        # @todo: Ugly. Why do we have to do this to refresh field values? I
        # guess we don't want to thrash the DB on every attribute access, but
        # still.
        basic_field = BasicField.objects.get(id=basic_field.id)
        self.assertEqual(basic_field.value, max)

    def test_create_new_mortal_sheet(self):
        """A blank sheet should start with a pretty big set of stats.
        """
        user = UserFactory()
        sheet = Sheet.objects.with_template('mortal', user)

        self.assertEqual(sheet.stat_set.count(), 9)
        self.assertEqual(sheet.skill_set.count(), 24)
        self.assertEqual(sheet.point_stat_set.count(), 3)
        self.assertEqual(sheet.misc_stat_set.count(), 5)
        self.assertEqual(sheet.supernatural_stat_set.count(), 0)
