from django.urls import path

from .views import RestaurantListView, RestaurantRetrieveView, RestaurantCreateView

urlpatterns = [
    path('', RestaurantListView.as_view(), name='restaurant_list'),
    path('create/', RestaurantCreateView.as_view(), name='restaurant_create'),
    path('<path:uuid>/', RestaurantRetrieveView.as_view(), name='restaurant_retrieve'),
]
