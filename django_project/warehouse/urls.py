from django.urls import path
from . import views
from part import views as partView

urlpatterns = [
    path("manage/warehouse", views.warehouse, name="warehouse"),
]