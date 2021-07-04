from django.urls import path
from . import views





urlpatterns = [
    path('registerforRaffle/', views.registerFor_RaffleDraw.as_view(), name='register-for-raffle'),
    path('raffleDraw-callback/', views.raffleDraw_callback,name='raffleDraw-callback'),
    path('allplayers/',views.List_Of_AllPlayers.as_view(), name='allplayers'),
]