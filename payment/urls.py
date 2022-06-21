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
from django.urls import path, include
from . import views


app_name = 'payment'


urlpatterns = [
    path("<str:imdbID>/order/", views.orderDetails, name='orderDetails'),
    path('thanks/', views.thanks, name='thanks'),
    path('checkout/<str:imdbID>/', views.checkout, name='checkout'),
    # path('stripe_webhook/', views.stripe_webhook, name='stripe_webhook')
]