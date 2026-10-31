from django.urls import path

from . import views


urlpatterns = [
    path("reports/", views.reports, name="reports"),
    path("reports/export.csv", views.reportsExport, name="reports export"),
]
