from django.utils import timezone
from rest_framework import generics

from api.mixins import AuthPermissionMixin
from .models import MenuVote
from .serializers import MenuVoteCreateSerializerV1, MenuVoteCreateSerializerV2, MenuVoteListTodaySerializer


class MenuVoteMixin:
    queryset = MenuVote.objects.all()


class MenuVoteCreateViewV1(AuthPermissionMixin, MenuVoteMixin, generics.CreateAPIView):
    serializer_class = MenuVoteCreateSerializerV1


class MenuVoteCreateViewV2(AuthPermissionMixin, MenuVoteMixin, generics.CreateAPIView):
    serializer_class = MenuVoteCreateSerializerV2


class MenuVoteListTodayView(AuthPermissionMixin, generics.ListAPIView):
    serializer_class = MenuVoteListTodaySerializer
    now = timezone.localtime(timezone.now())
    today = now.date()
    queryset = MenuVote.objects.filter(created_at__date=today).order_by('created_at')
