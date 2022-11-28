from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("warehouse", views.warehouse, name="warehouse"),
    path("storage", views.storage, name="storage"),
    path("shelf", views.shelf, name="shelf"),
    path("compartment", views.compartment, name="compartment"),
]
