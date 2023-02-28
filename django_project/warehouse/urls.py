from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("warehouse/add", views.addWarehouse, name="warehouses"),
    path("warehouse/", views.warehouses, name="warehouses"),
    path("storage/add", views.addStorage, name="storages"),
    path("storage/", views.storages, name="storages"),
    path("shelf/add", views.addShelf, name="shelfs"),
    path("shelf/", views.shelfs, name="shelfs"),
    path("compartment/add", views.addCompartment, name="compartments"),
    path("compartment/", views.compartments, name="compartments"),
]
