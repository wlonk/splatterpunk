from django.db import (
    models,
    transaction,
)

from .constants import (
    STAT_NAMES,
    SKILL_NAMES,
    POINT_STAT_NAMES,
    DERIVED_STAT_NAMES,
    SHEET_TEMPLATES,
)


class SheetQuerySet(models.query.QuerySet):

    def with_template(self, template_name, user, name=''):
        from .models import (
            BasicField,
            PointsField,
            TextField,
        )
        template = SHEET_TEMPLATES[template_name]
        with transaction.atomic():
            sheet = self.create(user=user, name=name)
            for key in STAT_NAMES:
                BasicField.objects.create(
                    sheet=sheet,
                    key=key,
                    value=1,
                    max=5
                )
            for key in SKILL_NAMES:
                BasicField.objects.create(
                    sheet=sheet,
                    key=key,
                    value=0,
                    max=5
                )
            for key in POINT_STAT_NAMES:
                PointsField.objects.create(
                    sheet=sheet,
                    key=key,
                    value=5,
                    max=10,
                    points=5
                )
            for key in DERIVED_STAT_NAMES:
                TextField.objects.create(
                    sheet=sheet,
                    key=key
                )
            for field in template:
                field.sheet = sheet
                field.save()
            return sheet


class SheetManager(models.Manager):
    def get_query_set(self):
        ret = SheetQuerySet(self.model)
        return ret

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)
