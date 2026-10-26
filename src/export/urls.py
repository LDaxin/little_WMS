from django.urls import path
from . import views


urlpatterns = [
    path("qr/print", views.qrPrint, name="qr print"),
]
