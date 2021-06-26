from django.urls import path,include
from iffliateLanding_page import views
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as password_restviews


# app_name ='iffliate_landingPage'
urlpatterns = [
    
    path('',views.index,name ='home'),
    path('product/',views.product,name='product'),
    path('pricing/',views.pricing,name='pricing'),
    path('team/',views.ourTeam,name='team'),
    path('support/',views.support,name='support'),
    path('contactUs/',views.contactUs,name='contact-us'),
    path('signup/',views.signup,name='signup'),
    path('logout',LogoutView.as_view(template_name='iffliateLanding_page/logout.html'),name='logout'),
    # this api is responsible for Creating User
    path('api/create-user/', views.CreateUserApi.as_view(), name='create-user-api'),
    # this api is responsible for Logging User  in 
    path('api/signin-user/', views.SignInAPIView.as_view(), name='signin-user-api'),
    path('signin/',views.SignInView.as_view(),name='signin'),
    
    # this url is for the blog view
    path('blog/', views.BlogListView.as_view(), name='blog-list-view'),
    path('blog-detail/<int:pk>/', views.BlogDetailView.as_view(), name='blog-detail'),

    # error page url
    path('error/', views.errorpage, name='errorpage'),

    # this path is a funtion based api view that takes care of payment
    path('accept-payment/', views.accept_paymentfor_anyplan),
    path('mycallback/', views.mycallback),

    path('password_reset/',views.password_reset_request,name='custom_password_reset'),
    path('reset-password/reset/<uidb64>/<token>/',views.CustomPasswordResetConfirmView.as_view()),
     path('reset-password/', include('django.contrib.auth.urls')),


]