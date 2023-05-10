from django.urls import path, re_path
from . import views


urlpatterns = [
    path("movement/", views.movement, name="movment"),
    path("movement/request/", views.movementCodeInfo, name="request"),
    #re_path(r'^article/(?P<typ>\w+)/(?P<article_id>[0-9]+)', views.article, name="article"),
    #re_path(r"^article/(?P<typ>\w+)/add", views.addArticle, name="add Article"),
]
