from django.urls import path
from . import views


urlpatterns = [
    path("part", views.part, name="part"),
    path("tag", views.tag, name="tag"),
    
    # path("part/", partView.part, name="part"),
]
