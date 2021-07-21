from django.urls import path
from users import views as user_views
from raffleDraw import views as raffle_views
import users

urlpatterns = [
    
    path('',user_views.UserDashboard.as_view(),name='user-dashboard'),
    path('readpost/',user_views.UserReadPostForMoneyPage.as_view(),name='read-post-for-money-page'),
    path('readpost-detail/<int:pk>/',user_views.UserReadPostForMoneyPageDetailView.as_view(),name='read-post-for-money-detail-page'),
    path('user-transactions/', user_views.UserTransactionPage.as_view(), name='user-transction'),
    # this is the first process to get payed u will have to file for a payment 
    # that if u are Eligble
    path('registerPayment/',user_views.FileForPayment.as_view(),name='file-for-payment'),

    # url for the ADMIN DASHBOARD
    path('adminDashboard/',user_views.AdminDashhboardIndex.as_view(), name='adminDasboard'),
    path('adminDashboard/listofpendingpayment/',user_views.UserRequestPaymentListView.as_view(), name='listofpendingpayment'),
    path('adminDashboard/payuser/<int:pk>/',user_views.PayUser.as_view(), name='payUSer'),
    path('adminDashboard/listallusers/',user_views.AllUserListView.as_view(), name='allUsers'),
    path('adminDashboard/deleteuser/<int:pk>/',user_views.DeleteUserView.as_view(), name='deleteUser'),
    # this is link that display the List Of Al l Raffle Draw
    path('adminDashboard/all_raffle_draw/',raffle_views.ListOfRaffleDraw.as_view(),name='AllRaffleDraw'),
    path('adminDashboard/raffleDrawDetail/<int:pk>/',raffle_views.RaffleDrawDetail.as_view(),name='RaffleDrawDetail'),
    path('adminDashboard/Close_RaffleDraw/<int:pk>/',raffle_views.Close_RaffleDrawView,name='Close_RaffleDraw'),
    # link to create a new raffle Draw exclusive_to_the adminUser
    path('adminDashboard/Create_Raffle_Draw_game/',raffle_views.Create_RaffleDrawView,name='create_raffle_draw'),
    path('adminDashboard/startCron/',user_views.StartCronJobView,name='start_cron_job'),
    # TEST URL DOWN HERE
    path('mywebhook/',user_views.payUserWebHook)
]

