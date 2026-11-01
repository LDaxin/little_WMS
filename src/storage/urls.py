from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^storage/search", views.searchStoragesAll, name="search storages all"),
    re_path(r"^storage/$", views.storagesAll, name="storages all"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/update", views.updateStorage, name="update Storage"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/store-search", views.storeArticleSearch, name="store article search"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/store", views.storeInStorage, name="store in Storage"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/remove/(?P<articleId>[0-9]+)", views.removeFromStorage, name="remove from Storage"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/tags/add", views.addStorageTag, name="add storage tag"),
    re_path(r"^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/tags/remove/(?P<tagId>[0-9]+)", views.removeStorageTag, name="remove storage tag"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/images/add', views.addStorageImage, name="add storage image"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/images/(?P<imageId>[0-9]+)/delete', views.deleteStorageImage, name="delete storage image"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/images/(?P<imageId>[0-9]+)/primary', views.setPrimaryStorageImage, name="set primary storage image"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)/i', views.storageIncert, name="storage"),
    re_path(r'^storage/(?P<typ>\w+)/(?P<storageId>[0-9]+)', views.storage, name="storage"),
    re_path(r"^storage/(?P<typ>\w+)/add/modal", views.addModal, name="add Storage Modal"),
    re_path(r"^storage/(?P<typ>\w+)/add", views.addStorage, name="add Storage"),
    re_path(r"^storage/(?P<typ>\w+)/del/modal", views.delModal, name="del Storage Modal"),
    re_path(r"^storage/(?P<typ>\w+)/del", views.delStorage, name="del Storage"),
    re_path(r"^storage/(?P<typ>\w+)/search", views.searchStorages, name="search"),
    re_path(r"^storage/(?P<typ>\w+)/export", views.exportStorages, name="storages export"),
    re_path(r"^storage/(?P<typ>\w+)/scanner/(?P<scannerId>\w+)/(?P<state>\w+)", views.storageScanner, name="storages scanner"),
    re_path(r"^storage/(?P<typ>\w+)/", views.storages, name="storages"),
]

