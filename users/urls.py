from django.urls import path
from users import views as user_views

urlpatterns = [
    
    path('',user_views.UserDashboard.as_view(),name='user-dashboard'),
    path('readpost/',user_views.UserReadPostForMoneyPage.as_view(),name='read-post-for-money-page'),
    path('readpost-detail/<int:pk>/',user_views.UserReadPostForMoneyPageDetailView.as_view(),name='read-post-for-money-detail-page'),
    path('user-transactions/', user_views.UserTransactionPage.as_view(), name='user-transction'),

]