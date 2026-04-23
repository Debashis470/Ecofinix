from django.urls import path
from . import views

urlpatterns = [
    path("", views.tax_home, name="tax_home"),
    path("calculator/", views.tax_calculator, name="tax_calc"),
    path("compare/", views.regime_compare, name="tax_compare"),
    path("policies/", views.policy_list, name="tax_policies"),
    path("upload/", views.policy_upload, name="policy_upload"),
]