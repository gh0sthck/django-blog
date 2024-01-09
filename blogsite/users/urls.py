from typing import List

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import user_page, registration, edit

urlpatterns: List = [
    # path("login/", login_page, name="login_page"),

    path("login/", auth_views.LoginView.as_view(
        template_name="user_login.html",
    ), name="login_page"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="user_logout.html",
    ), name="logout_page"),

    path("register/", registration, name="register"),
    path("edit/", edit, name="edit"),

    path("<int:user_id>/", user_page, name="user_page"),
]