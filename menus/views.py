from django.db.models import Q
from django.utils import timezone
from rest_framework import generics

from api.mixins import AdminPermissionMixin, AuthPermissionMixin
from .models import Menu
from .serializers import MenuRetrieveSerializer, MenuCreateSerializer, MenuListSerializer


class MenuMixin:
    queryset = Menu.objects.all()


class MenuCreateView(AdminPermissionMixin, MenuMixin, generics.CreateAPIView):
    serializer_class = MenuCreateSerializer


class MenuRetrieveView(AuthPermissionMixin, MenuMixin, generics.RetrieveAPIView):
    serializer_class = MenuRetrieveSerializer
    lookup_field = 'uuid'


class MenuListTodayView(AuthPermissionMixin, generics.ListAPIView):
    serializer_class = MenuListSerializer
    today = timezone.now().date()

    queryset = Menu.objects.filter(
        Q(published_for=today) &
        Q(active=True)
    ).order_by('restaurant_id')
