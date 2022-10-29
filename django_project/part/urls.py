from django.urls import path
from . import views


urlpatterns = [
    path("manage/part", views.part, name="part"),
    path("manage/tag", views.tag, name="tag"),
    
    # path("part/", partView.part, name="part"),
]
