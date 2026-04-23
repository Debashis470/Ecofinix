from django.urls import path
from . import views

urlpatterns = [
    path('', views.investment_dashboard, name='investment_dashboard'),
]
