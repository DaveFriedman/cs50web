from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_entry, name="create"),
    path("create/<str:title>", views.create_entry, name="create"),
    path("wiki/<str:title>", views.read_entry, name="read"),
    path("wiki/<str:title>/update", views.update_entry, name="update"),
    path("wiki/<str:title>/delete", views.delete_entry, name="delete"),
    path("search", views.search, name="search"),
    path("random", views.random, name="random"),
]
