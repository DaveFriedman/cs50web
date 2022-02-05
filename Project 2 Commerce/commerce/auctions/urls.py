from django.urls import path

from . import views

urlpatterns = [
    path("",                    views.index,            name="index"),

    path("create",              views.create_listing,   name="create"),
    path("<str:category>",      views.read_category,    name="category"),
    path("<int:id>/<str:name>", views.read_listing,     name="read"),
    path("watchlist",           views.read_watchlist,   name="watchlist"),
    path("<int:id>/<str:name>/watchlist", views.watch,  name="watch"),
    # path("close",               views.close_listing,    name="close"),

    path("random",              views.random,           name="random"),
    path("search",              views.search,           name="search"),
    
    path("login",               views.login_view,       name="login"),
    path("logout",              views.logout_view,      name="logout"),
    path("register",            views.register,         name="register")
]
