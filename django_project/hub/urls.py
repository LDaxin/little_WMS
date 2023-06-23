from django.urls import path
from . import views


urlpatterns = [
    path("",views.hub, name="hub"),
    path("module/search/results", views.results, name="results"),
]
