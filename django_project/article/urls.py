from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^article/(?P<typ>\w+)/(?P<articleId>[0-9]+)/update', views.updateArticle, name="update article"),
    re_path(r'^article/(?P<typ>\w+)/(?P<articleId>[0-9]+)/i', views.articleIncert, name="article"),
    re_path(r'^article/(?P<typ>\w+)/(?P<articleId>[0-9]+)', views.article, name="article"),
    re_path(r"^article/(?P<typ>\w+)/add/modal", views.addModal, name="add Article Modal"),
    re_path(r"^article/(?P<typ>\w+)/add", views.addArticle, name="add Article"),
    re_path(r"^article/(?P<typ>\w+)/del/modal", views.delModal, name="del Article Modal"),
    re_path(r"^article/(?P<typ>\w+)/del", views.delArticle, name="del Article"),
    re_path(r"^article/(?P<typ>\w+)/upadte", views.delArticle, name="del Article"),
    re_path(r"^article/(?P<typ>\w+)/search", views.searchArticle, name="search"),
    re_path(r"^article/(?P<typ>\w+)/export", views.exportArticles, name="articles export"),
    re_path(r"^article/(?P<typ>\w+)/scanner/(?P<scannerId>\w+)/(?P<state>\w+)", views.articleScanner, name="articles scanner"),
    re_path(r"^article/(?P<typ>\w+)/", views.articles, name="articles"),
]
