from django.contrib.auth import get_user_model
from rest_framework import generics

from api.mixins import AdminPermissionMixin
from .serializers import (ParticipantListSerializer, ParticipantCreateSerializer, ParticipantRetrieveSerializer)

User = get_user_model()


class ParticipantMixin(AdminPermissionMixin):
    queryset = User.objects.all()


class ParticipantListView(ParticipantMixin, generics.ListAPIView):
    serializer_class = ParticipantListSerializer


class ParticipantCreateView(ParticipantMixin, generics.CreateAPIView):
    serializer_class = ParticipantCreateSerializer


class ParticipantRetrieveView(ParticipantMixin, generics.RetrieveAPIView):
    serializer_class = ParticipantRetrieveSerializer
