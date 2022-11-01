from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("manage/warehouse", views.warehouse, name="warehouse"),
    path("manage/storage", views.storage, name="storage"),
    path("manage/shelf", views.shelf, name="shelf"),
    path("manage/compartment", views.compartment, name="compartment"),
]
