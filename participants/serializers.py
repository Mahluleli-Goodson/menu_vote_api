from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from participants import validators

User = get_user_model()


class ParticipantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups']


class ParticipantCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(validators=[validators.validate_strong_password])
    email = serializers.EmailField(validators=[validators.validate_unique_email], required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'email']

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        instance = super().create(validated_data)
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation.pop('password', None)  # Exclude 'password' field from serialized output
        return representation


class ParticipantRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'groups']
