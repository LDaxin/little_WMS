from django.urls import path
from . import views


urlpatterns = [
    path("",views.hub, name="hub"),
    path("manage/",views.manage, name="manage"),
    path("manage/location", views.locations, name="locations"),
    
    # path("part/", partView.part, name="part"),
]
