from rest_framework import permissions, generics

from api.mixins import AuthPermissionMixin
from .models import Restaurant
from .serializers import RestaurantListSerializer, RestaurantRetrieveSerializer, RestaurantCreateSerializer


class RestaurantMixin:
    queryset = Restaurant.objects.all()


class RestaurantListView(AuthPermissionMixin, RestaurantMixin, generics.ListAPIView):
    serializer_class = RestaurantListSerializer


class RestaurantCreateView(AuthPermissionMixin, generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = RestaurantCreateSerializer


class RestaurantRetrieveView(AuthPermissionMixin, RestaurantMixin, generics.RetrieveAPIView):
    serializer_class = RestaurantRetrieveSerializer
    lookup_field = 'uuid'
