from rest_framework import serializers

from menus.models import Menu
from restaurants.models import Restaurant
from restaurants.serializers import RestaurantRetrieveSerializer


class MenuCreateSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(
        required=True,
        queryset=Restaurant.objects.all()
    )
    description = serializers.CharField(style={'base_template': 'textarea.html'}, required=True)

    class Meta:
        model = Menu
        fields = ['title', 'restaurant', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance and instance.uuid:
            representation['restaurant'] = instance.restaurant.uuid
            representation['uuid'] = instance.uuid
        return representation


class MenuRetrieveSerializer(serializers.ModelSerializer):
    restaurant = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ['uuid', 'title', 'restaurant', 'description']

    def get_restaurant(self, instance):
        if instance and instance.restaurant:
            return RestaurantRetrieveSerializer(
                instance=instance.restaurant,
                read_only=True,
                context=self.context,
            ).data
        return None


class MenuListSerializer(MenuRetrieveSerializer):
    pass
