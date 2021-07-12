from django.urls import path
from . import views





urlpatterns = [
    path('registerforRaffle/', views.registerFor_RaffleDraw.as_view(), name='register-for-raffle'),
    path('raffleDraw-callback/', views.raffleDraw_callback,name='raffleDraw-callback'),
    path('countdown-to-game/',views.countDown,name='countDown'),

    # This is api view urls
    # this is to check if it time for a mae or  not -- if it true redirect the user to the payment page
    # path('api/check_if_it_time_for_game',views.check_batchDate,name='checkGameEvent')
]