from django.urls import path

from . import views


urlpatterns = [
    path("views/", views.savedViews, name="saved views"),
    path("views/save/", views.saveSavedView, name="save saved view"),
    path("views/<int:viewId>/delete/", views.delSavedView, name="delete saved view"),
    path("views/<int:viewId>/dashboard/", views.toggleDashboard, name="toggle dashboard view"),
    path("views/<int:viewId>/share/", views.shareSavedView, name="share saved view"),
    path("share-links/<int:linkId>/revoke/", views.revokeShareLink, name="revoke share link"),
    path("s/<str:token>/", views.shareLinkView, name="share link"),
]
