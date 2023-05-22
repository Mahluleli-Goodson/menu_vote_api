from django.urls import path

from participants.views import ParticipantListView, ParticipantRetrieveView, ParticipantCreateView

urlpatterns = [
    path('', ParticipantListView.as_view(), name='user_list'),
    path('create/', ParticipantCreateView.as_view(), name='user_create'),
    path('<int:pk>/', ParticipantRetrieveView.as_view(), name='user_retrieve'),
]
