"""Moviepedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path

from . import views

app_name = 'Movie'

urlpatterns = [
    path("", views.publicIndex, name='publicIndex'),

    path("userSignup/", views.userSignup, name='userSignup'),

    path("userLogin/", views.userLogin, name='userLogin'),

    path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path("userDetails/", views.userDetails, name='userDetails'),

    path("updateUser/", views.updateUser, name='updateUser'),

    path("userOrders/", views.userOrders, name='userOrders'),

    path("order/<str:username>/<str:imdbID>/", views.userOrderdetail, name='userOrderdetail'),

    path("userLogout/", views.userLogout, name='userLogout'),

]
