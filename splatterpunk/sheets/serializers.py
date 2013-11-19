from django.contrib.auth import get_user_model

from rest_framework import serializers

from .models import Sheet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()


class SheetSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Sheet
