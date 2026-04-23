# savings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & analyze are now handled by the same view
    path("", views.savings_dashboard, name="savings_home"),
    path("analyze/", views.savings_dashboard, name="savings_analyze"),
]