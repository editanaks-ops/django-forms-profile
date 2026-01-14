from django.urls import path
from django.shortcuts import redirect
from .views import (
    register_view,
    login_view,
    logout_view,
    profile_view,
    message_create_view,
)

urlpatterns = [
    path("", lambda request: redirect("login"), name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile_view, name="profile"),
    path("message/", message_create_view, name="message"),
]

