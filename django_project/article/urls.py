from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^article/(?P<typ>\w+)/(?P<article_id>[0-9]+)/i', views.articleIncert, name="article"),
    re_path(r'^article/(?P<typ>\w+)/(?P<article_id>[0-9]+)', views.article, name="article"),
    re_path(r"^article/(?P<typ>\w+)/add", views.addArticle, name="add Article"),
    re_path(r"^article/(?P<typ>\w+)/del", views.delArticle, name="del Article"),
    re_path(r"^article/(?P<typ>\w+)/", views.articles, name="articles"),
    path("tag", views.tag, name="tag"),
]
