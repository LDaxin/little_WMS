from django.urls import path, re_path
from . import views, inventory


urlpatterns = [
    path("movement/", views.movement, name="movement"),
    path("inventory/", inventory.inventory, name="inventory"),
    path("inventory/scan/", inventory.inventoryScan, name="inventory scan"),
    path("inventory/search/", inventory.inventorySearch, name="inventory search"),
    path("inventory/clear/", inventory.inventoryClear, name="inventory clear"),
    path("inventory/export/", inventory.inventoryExport, name="inventory export"),
    path("where/", views.where, name="where"),
    path("where/search", views.whereSearch, name="where search"),
    path("where/scanner/<str:scannerId>/<str:state>", views.movementScanner, name="where scanner"),
    path("movement/scan/", views.movementScan, name="movement scan"),
    path("movement/mode/", views.movementMode, name="movement mode"),
    path("movement/clear/", views.movementClear, name="movement clear"),
    path("movement/buffer/remove/", views.movementBufferRemove, name="movement buffer remove"),
    path("movement/target/clear/", views.movementTargetClear, name="movement target clear"),
    path("movement/treat-as-article/", views.movementTreatAsArticle, name="movement treat as article"),
    path("movement/set-target/", views.movementSetTarget, name="movement set target"),
    path("movement/store/", views.movementStore, name="movement store"),
    path("movement/remove/", views.movementRemove, name="movement remove"),
    path("movement/undo/", views.movementUndo, name="movement undo"),
    path("movement/undo/entry/", views.movementUndoEntry, name="movement undo entry"),
    path("movement/search/", views.movementSearch, name="movement search"),
    re_path(r"^movement/scanner/(?P<scannerId>\w+)/(?P<state>\w+)", views.movementScanner, name="movement scanner"),
]
