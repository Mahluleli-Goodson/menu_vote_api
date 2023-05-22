from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

User = get_user_model()

validate_unique_email = UniqueValidator(queryset=User.objects.all(), lookup='iexact')


def validate_strong_password(value):
    try:
        validate_password(value)
    except Exception as exc:
        raise serializers.ValidationError(exc.messages)
    return value
