from django.urls import path, re_path
from . import views


urlpatterns = [
    path("movement/", views.movement, name="movement"),
    path("where/", views.where, name="where"),
    path("movement/scan/", views.movementScan, name="movement scan"),
    path("movement/mode/", views.movementMode, name="movement mode"),
    path("movement/clear/", views.movementClear, name="movement clear"),
    path("movement/buffer/remove/", views.movementBufferRemove, name="movement buffer remove"),
    path("movement/target/clear/", views.movementTargetClear, name="movement target clear"),
    path("movement/treat-as-article/", views.movementTreatAsArticle, name="movement treat as article"),
    path("movement/set-target/", views.movementSetTarget, name="movement set target"),
    path("movement/store/", views.movementStore, name="movement store"),
    path("movement/remove/", views.movementRemove, name="movement remove"),
    path("movement/search/", views.movementSearch, name="movement search"),
    re_path(r"^movement/scanner/(?P<scannerId>\w+)/(?P<state>\w+)", views.movementScanner, name="movement scanner"),
]
