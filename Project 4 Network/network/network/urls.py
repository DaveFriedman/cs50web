from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("following", views.following, name="following"),
    path("u/<int:profileid>/<str:profilename>", views.profile, name="profile"),
    path("p/<int:postid>", views.read_post, name="read_post"),
    path("post", views.create_post, name="create_post"),
    path("p/<int:postid>/edit", views.edit_post, name="edit_post"),
    path("p/<int:postid>/delete", views.delete_post, name="delete_post"),
    path("p/<int:postid>/like", views.like_post, name="like_post"),
    path("p/<int:postid>/dislike", views.dislike_post, name="dislike_post"),
    path("follow/<int:profileid>/", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("settings", views.account_settings, name="settings"),
    path("settings/password", views.change_account_password, name="password"),
]
