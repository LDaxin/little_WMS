from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("warehouse/add", views.addWarehouse, name="add warehouses"),
    path("warehouse/del", views.delWarehouse, name="del warehouses"),
    path("warehouse/", views.warehouses, name="warehouses"),
    path("storage/add", views.addStorage, name="add storages"),
    path("storage/del", views.delStorage, name="del storages"),
    path("storage/", views.storages, name="storages"),
    path("shelf/add", views.addShelf, name="add shelfs"),
    path("shelf/del", views.delShelf, name="del shelfs"),
    path("shelf/", views.shelfs, name="shelfs"),
    path("compartment/add", views.addCompartment, name="add compartments"),
    path("compartment/del", views.delCompartment, name="del compartments"),
    path("compartment/", views.compartments, name="compartments"),
]
