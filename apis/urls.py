from django.urls import include, path
from rest_framework import routers, urls

from . import views


urlpatterns = [

    path('user/reset_password/', views.reset_password),

    path('user/login/', views.LoginView.as_view()),
    path('user/logout/', views.log_out_view),
    path('user/register/', views.register_user_api_view),
    path('user/me/', views.authenticatedUser),

    path('user/', views.get_all_user_api_view),
    path('user/<int:id>/', views.get_one_user_api_view),

]
