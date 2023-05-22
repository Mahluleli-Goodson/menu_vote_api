from rest_framework import serializers

from .models import AccessKey


class AccessKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessKey
        fields = ['resource_key', 'secret_key']
