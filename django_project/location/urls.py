from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^location/(?P<locationId>[0-9]+)/i', views.locationIncert, name="location"),
    re_path(r'^location/(?P<locationId>[0-9]+)', views.location, name="location"),
    path("location/add", views.addLocation, name="add Locations"),
    path("location/del", views.delLocation, name="del Locations"),
    path("location/", views.locations, name="locations"),
]