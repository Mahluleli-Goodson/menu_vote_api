from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from restaurants.models import Restaurant
from restaurants.serializers import RestaurantListSerializer, RestaurantCreateSerializer, RestaurantRetrieveSerializer


class RestaurantSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.restaurant = Restaurant.objects.create(label='Test Restaurant')

    def test_restaurant_list_serializer(self):
        serializer = RestaurantListSerializer(instance=self.restaurant)
        expected_data = {
            'uuid': str(self.restaurant.uuid),
            'label': 'Test Restaurant',
        }
        self.assertEqual(serializer.data, expected_data)

    def test_restaurant_create_serializer(self):
        serializer = RestaurantCreateSerializer(data={'label': 'New Restaurant'})
        serializer.is_valid()
        restaurant = serializer.save()
        self.assertEqual(restaurant.label, 'New Restaurant')
        self.assertIsNotNone(restaurant.uuid)

    def test_restaurant_retrieve_serializer(self):
        serializer = RestaurantRetrieveSerializer(instance=self.restaurant, context={'request': self})
        expected_data = {
            'uuid': str(self.restaurant.uuid),
            'label': 'Test Restaurant',
        }
        self.assertEqual(serializer.data, expected_data)
