from django.urls import path

from . import views


urlpatterns = [
    path("occasions/", views.occasions, name="occasions"),
    path("occasions/add/", views.addOccasion, name="add occasion"),
    path("occasions/types/", views.occasionTypes, name="occasion types"),
    path("occasions/types/add/", views.addOccasionType, name="add occasion type"),
    path("occasions/<int:occasionId>/", views.occasion, name="occasion"),
    path("occasions/<int:occasionId>/update/", views.updateOccasion, name="update occasion"),
    path("occasions/<int:occasionId>/delete/", views.delOccasion, name="delete occasion"),
    path("occasions/<int:occasionId>/packlist/add/", views.packlistAdd, name="packlist add"),
    path("occasions/<int:occasionId>/packlist/<int:entryId>/status/", views.packlistStatus, name="packlist status"),
    path("occasions/<int:occasionId>/packlist/<int:entryId>/remove/", views.packlistRemove, name="packlist remove"),
]
