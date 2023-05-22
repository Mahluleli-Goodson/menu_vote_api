from rest_framework import serializers

from access_keys.serializers import AccessKeySerializer
from restaurants.models import Restaurant


class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['uuid', 'label']


class RestaurantCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['label']

    def to_representation(self, instance):
        if instance and instance.uuid:
            return RestaurantRetrieveSerializer(
                instance,
                read_only=True,
                context=self.context,
            ).data
        return super().to_representation(instance)


class RestaurantRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['uuid', 'label']

    def get_fields(self):
        fields = super().get_fields()
        user = self.context.get('request').user

        if user and user.is_staff:
            # if user is Admin then allow them to see access_keys
            fields['access_key'] = AccessKeySerializer(read_only=True)

        return fields
