
from django.urls import path, include
from . import views

urlpatterns = [

    path("board", views.index, name="index"),
    path("", views.user, name="user"),
]
