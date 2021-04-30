from django.urls import path
from iffliateLanding_page import views



# app_name ='iffliate_landingPage'
urlpatterns = [
    
    path('',views.index,name ='home'),
    path('product/',views.product,name='product'),
    path('pricing/',views.pricing,name='pricing'),
    path('team/',views.ourTeam,name='team'),
    path('support/',views.support,name='support'),
    path('contactUs/',views.contactUs,name='contact-us'),
    path('signup/',views.signup,name='signup'),
    path('api/create-user/', views.CreateUserApi.as_view(), name='create-user-api'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    
    # this url is for the blog view
    path('blog/', views.BlogListView.as_view(), name='blog-list-view'),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),



    # this path is a funtion based api view that takes care of payment
    path('accept-payment/', views.accept_paymentfor_anyplan),
    path('mycallback/', views.mycallback),
]