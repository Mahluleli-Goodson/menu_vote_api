from django.urls import path

from .views import MenuCreateView, MenuRetrieveView, MenuListTodayView

urlpatterns = [
    path('create/', MenuCreateView.as_view(), name='menu_create'),
    path('today/', MenuListTodayView.as_view(), name='menu_today'),
    path('<path:uuid>/', MenuRetrieveView.as_view(), name='menu_retrieve'),
]
