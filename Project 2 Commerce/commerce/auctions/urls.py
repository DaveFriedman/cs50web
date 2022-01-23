from django.urls import path

from . import views

urlpatterns = [
    path("",                    views.index,            name="index"),

    path("create",              views.create_listing,   name="create"),
    path("<int:id>/<str:name>", views.read_listing,     name="read"),
    path("<int:id>/update",     views.update_listing,   name="update"),
    path("<int:id>/delete",     views.delete_listing,   name="delete"),

    path("random",              views.random,           name="random"),
    path("search",              views.search,           name="search"),
    path("watchlist",           views.watchlist,        name="watchlist"),
    

    # possible change to /accounts/login, per
    # https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-LOGIN_URL 
    path("login",               views.login_view,       name="login"),
    path("logout",              views.logout_view,      name="logout"),
    path("register",            views.register,         name="register"),
]
