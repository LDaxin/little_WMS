from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("warehouse/", views.warehouses, name="warehouses"),
    path("storage/", views.storages, name="storages"),
    path("shelf/", views.shelfs, name="shelfs"),
    path("compartment/", views.compartments, name="compartments"),
]
