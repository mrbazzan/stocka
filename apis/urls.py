from django.urls import include, path, re_path
from rest_framework import routers, urls

from . import views


urlpatterns = [  
    path('user/password_reset_token/', views.password_reset),
    path('user/change_password/', views.change_password),
    path('user/reset_password/', views.reset, name="reset_password"),

    path('user/login/', views.LoginView.as_view()),
    path('user/logout/', views.log_out_view),
    path('user/register/', views.register_user_api_view, name="user_register"),
    path('user/me/', views.authenticatedUser),

    path('user/reset_confirm/', views.confirm_email, name="reset_confirm"),

    path('user/', views.get_all_user_api_view),
    path('user/<int:id>/', views.get_one_user_api_view),

]
