"""BusDepoManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from unicodedata import name
from django.contrib import admin
from django.urls import path, re_path
from BusDepoManagement import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homePage,name="home"),
    path('contactus/',views.contactPage,name="contact"),
    path('aboutus/',views.aboutPage,name="about"),
    path('loginPage/',views.loginPage,name="loginPage"),
    path('signOut/',views.signOut,name="signOut"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('registrationPage/',views.registrationPage,name="registrationPage"),
    path('timeTablePage/',views.timeTablePage,name="timeTablePage"),
    path('timeTablePage/<int:id>/',views.showBookPage, name="showBookPage"),
    path('payment_status/',views.payment_status,name="payment_status"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('payment_receipt/<str:bookBus>',views.payment_receipt,name="payment_receipt"),
]
