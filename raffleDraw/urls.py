from django.urls import path
from . import views





urlpatterns = [
    path('registerforRaffle/', views.registerFor_RaffleDraw.as_view(), name='register-for-raffle'),
    path('gameNotAvaliable/',views.Game_is_close_for_now,name='gameNotAvaliable')
]