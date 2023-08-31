"""
URL configuration for ecom_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('signup',views.signup,name='signup'),
    # path('otpverify',views.otp_verify,name='otpverify'),
    path('otpverify/<str:phone>,<int:id>',views.otp_verify,name='otpverify'),
    path('login',views.user_login,name='login'),
    path('admlogin',views.admin_login,name='admlogin'),
    path('admlogout',views.admlogout,name='admlogout'),
    path('logout',views.userlogout,name='logout'),
    path('forgotPass',views.forgot_pass,name='forgotPass'),
    path('forgotPass_otpVerify/<int:id>,<str:phone>,<str:password>',views.forgotPass_otpVerify,name='forgotPass_otpVerify'),
    
    path('test',views.test,name='test')
]
 