from django.urls import path

from . import views

urlpatterns = [
    path("",                    views.index,            name="index"),

    path("create",              views.create_listing,   name="create"),
    path("",      views.read_category,    name="category"),
    path("<int:id>/<str:name>", views.read_listing,     name="read"),
    # path("watchlist",           views.read_watchlist,   name="watchlist"),
    # path("close",               views.close_listing,    name="close"),

    path("random",              views.random,           name="random"),
    path("search",              views.search,           name="search"),
    
    path("login",               views.login_view,       name="login"),
    path("logout",              views.logout_view,      name="logout"),
    path("register",            views.register,         name="register")
]

    # possible change to /accounts/login, per
    # https://docs.djangoproject.com/en/4.0/ref/settings/#std:setting-LOGIN_URL 