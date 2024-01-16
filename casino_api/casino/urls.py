from django.urls import path
from . import views

urlpatterns = [
    path('getGames', views.get_games, name='get_games'),
    path('gameLaunch', views.game_launch, name='game_launch'),
    path('bet', views.bet, name='bet'),
    path('win', views.win, name='win'),
    path('refund', views.refund, name='refund'),
]
