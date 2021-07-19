from django.urls import path
from . import views
from django.conf import settings




urlpatterns = [
    path('registerforRaffle/', views.registerFor_RaffleDraw.as_view(), name='register-for-raffle'),
    path('gameNotAvaliable/',views.Game_is_close_for_now,name='gameNotAvaliable'),

    # NOTE THIS IS A DYNAMIC URL IT IS THE CALL BACK FOR RAFFLE PAYMENT WE SET IT IN THE SETTINGS
    path('raffleDraw-callback/',views.raffle_paymentcallback)
]