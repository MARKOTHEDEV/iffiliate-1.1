from django.urls import path
from . import views





urlpatterns = [
    path('registerforRaffle/', views.registerFor_RaffleDraw, name='register-for-raffle'),
]