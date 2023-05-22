from rest_framework import generics

from api.mixins import AuthPermissionMixin
from .models import MenuScore
from .serializers import MenuScoreSerializer


class MenuScoreListView(AuthPermissionMixin, generics.ListAPIView):
    queryset = MenuScore.objects.all()
    serializer_class = MenuScoreSerializer
