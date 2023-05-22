from rest_framework import serializers

from .models import MenuScore


class MenuScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuScore
        fields = ['label', 'uuid']
