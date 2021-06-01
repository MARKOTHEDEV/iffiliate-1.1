from django.urls import path
from users import views as user_views

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

]