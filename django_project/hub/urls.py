from django.urls import path
from . import views
from part import views as partView


urlpatterns = [
    path("",views.hub, name="hub"),
    path("part/", partView.part, name="part"),
]