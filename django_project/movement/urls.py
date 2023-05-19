from django.urls import path, re_path
from . import views


urlpatterns = [
    path("movement/", views.movement, name="movment"),
    path("movement/request/", views.movementCodeInfo, name="request"),
    path("movement/store/", views.movementStore, name="store"),
    path("movement/remove/", views.movementRemove, name="remove"),
]
