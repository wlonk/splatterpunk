from django.conf import settings
from django.db import models


class Sheet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=255, blank=True)
