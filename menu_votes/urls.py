from django.urls import path

from menu_scores.views import MenuScoreListView
from .views import MenuVoteCreateViewV1, MenuVoteCreateViewV2, MenuVoteListTodayView

urlpatterns = [
    path('api/menu/scores/', MenuScoreListView.as_view(), name='menu_scores'),
    path('api/menu/vote/today', MenuVoteListTodayView.as_view(), name='menu_vote_today'),
    path('api/v1/menu/vote/', MenuVoteCreateViewV1.as_view(), name='menu_vote_v1'),
    path('api/v2/menu/vote/', MenuVoteCreateViewV2.as_view(), name='menu_vote_v2'),
]
