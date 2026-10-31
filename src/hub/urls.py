from django.urls import path
from . import views


urlpatterns = [
    path("",views.hub, name="hub"),
    path("trash/", views.trash, name="trash"),
    path("trash/<int:contentTypeId>/<str:objectId>/restore/", views.trashRestore, name="trash restore"),
    path("trash/<int:contentTypeId>/<str:objectId>/delete/", views.trashDeleteForever, name="trash delete forever"),
]
