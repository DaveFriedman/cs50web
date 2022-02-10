from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category/<str:category>", views.read_category, name="category"),
    path("create", views.create_listing, name="create"),
    path("<int:id>/<str:name>", views.read_listing, name="read"),
    path("<int:id>/<str:name>/bid", views.create_bid, name="bid"),
    path("<int:id>/<str:name>/comment>", views.create_comment, name="comment"),
    path("<int:id>/<str:name>/close", views.close_listing, name="close"),
    path("<int:id>/<str:name>/watchlist", views.watch, name="watch"),
    path("watchlist", views.read_watchlist, name="watchlist"),
    path("accounts/login", views.login_view, name="login"),
    path("accounts/logout", views.logout_view, name="logout"),
    path("accounts/register", views.register, name="register"),
]
