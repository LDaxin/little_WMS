from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/update", views.updateStorage, name="update Storage"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/i', views.storageIncert, name="storage"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)', views.storage, name="storage"),
    re_path(r"^storage/(?P<typ>\w+)/add/modal", views.addModal, name="add Storage Modal"),
    re_path(r"^storage/(?P<typ>\w+)/add", views.addStorage, name="add Storage"),
    re_path(r"^storage/(?P<typ>\w+)/del/modal", views.delModal, name="del Storage Modal"),
    re_path(r"^storage/(?P<typ>\w+)/del", views.delStorage, name="del Storage"),
    re_path(r"^storage/(?P<typ>\w+)/search", views.searchStorages, name="search"),
    re_path(r"^storage/(?P<typ>\w+)/export", views.exportStorages, name="storages export"),
    re_path(r"^storage/(?P<typ>\w+)/", views.storages, name="storages"),
]

