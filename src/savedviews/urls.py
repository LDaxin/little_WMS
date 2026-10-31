from django.urls import path

from . import views


urlpatterns = [
    path("views/", views.savedViews, name="saved views"),
    path("views/save/", views.saveSavedView, name="save saved view"),
    path("views/<int:viewId>/delete/", views.delSavedView, name="delete saved view"),
]
