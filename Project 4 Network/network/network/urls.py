
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("feed", views.feed, name="feed"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("settings", views.account_settings, name="settings"),
    path("u/<int:userid>/<str:username>", views.account_profile, name="profile"),
]
