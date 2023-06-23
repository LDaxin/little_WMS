from django.urls import path
from . import views


urlpatterns = [
    path("location/add", views.addLocation, name="add Locations"),
    path("location/del", views.delLocation, name="del Locations"),
    path("location/", views.locations, name="locations"),
]
