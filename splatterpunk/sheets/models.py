from django.conf import settings
from django.db import models


class Sheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255, blank=True)


class TextField(models.Model):
    sheet = models.ForeignKey(Sheet)
    key = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)


class BasicField(models.Model):
    sheet = models.ForeignKey(Sheet)
    key = models.CharField(max_length=255, blank=True)
    value = models.PositiveSmallIntegerField()
    max = models.PositiveSmallIntegerField()

    def clean(self):
        if self.value > self.max:
            self.value = self.max

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class SpecialtyField(models.Model):
    field = models.ForeignKey(BasicField)
    key = models.CharField(max_length=255, blank=True)


class PointsField(models.Model):
    sheet = models.ForeignKey(Sheet)
    key = models.CharField(max_length=255, blank=True)
    value = models.PositiveSmallIntegerField()
    max = models.PositiveSmallIntegerField()
    points = models.PositiveSmallIntegerField()

    def clean(self):
        if self.value > self.max:
            self.value = self.max
        if self.points > self.value:
            self.points = self.value

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class HealthField(models.Model):
    sheet = models.ForeignKey(Sheet)
    key = models.CharField(max_length=255, blank=True)
    max = models.PositiveSmallIntegerField(default=7)
    bashing = models.PositiveSmallIntegerField(default=0)
    lethal = models.PositiveSmallIntegerField(default=0)
    aggravated = models.PositiveSmallIntegerField(default=0)

    def clean(self):
        while (self.bashing + self.lethal + self.aggravated > self.max):
            if self.bashing > 0:
                self.bashing -= 1
            elif self.lethal > 0:
                self.lethal -= 1
            elif self.aggravated > 0:
                self.aggravated -= 1

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)

    def _add_helper(self, field, amount):
        # @todo: we could make this immune to race conditions, but when are
        # multiple people updating the same sheet?
        try:
            value = getattr(self, field)
            setattr(self, field, value + amount)
        except AttributeError:
            return
        else:
            self.save()

    def add_bashing(self, amount=1):
        self._add_helper('bashing', amount)

    def add_lethal(self, amount=1):
        self._add_helper('lethal', amount)

    def add_aggravated(self, amount=1):
        self._add_helper('aggravated', amount)
