from django.urls import include, path
from . import views
 


urlpatterns = [
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),

    path("dashboard/", views.dashboard_view, name="dashboard"),
    path("emi/", views.emi_view, name="emi"),

    path("loan/", views.loan_predict_view, name="loan"),
    path("planner/", views.credit_planner_view, name="credit_planner"),
    path("savings/", views.savings_view, name="savings"),

    path("tax/", include("tax.urls")),

    path("loan-prediction/", views.loan_predict_view, name="loan_prediction"),
    
   path ("emi-dashboard/", views.emi_view2, name="emi_dashboard"),
   path ("emi-list/", views.emi_list_view, name="emi_list"),
]