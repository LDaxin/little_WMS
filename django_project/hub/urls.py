from django.urls import path
from . import views


urlpatterns = [
    path("",views.hub, name="hub"),
    path("location/add", views.addLocation, name="add Locations"),
    path("location/del", views.delLocation, name="del Locations"),
    path("location/", views.locations, name="locations"),
    path("module/search/results", views.results, name="results"),
]
