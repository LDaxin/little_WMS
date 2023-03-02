from django.urls import path, re_path
from . import views


urlpatterns = [
    re_path(r'^part/(?P<typ>\w+)/(?P<part_id>[0-9]+)/i', views.partIncert, name="part"),
    re_path(r'^part/(?P<typ>\w+)/(?P<part_id>[0-9]+)', views.part, name="part"),
    re_path(r"^part/(?P<typ>\w+)/add", views.addPart, name="add Part"),
    re_path(r"^part/(?P<typ>\w+)/del", views.delPart, name="del Part"),
    re_path(r"^part/(?P<typ>\w+)/", views.parts, name="parts"),
    path("tag", views.tag, name="tag"),
]
