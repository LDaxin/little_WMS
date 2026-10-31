from django.urls import path

from . import views


urlpatterns = [
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/<int:notificationId>/read/", views.notificationRead, name="notification read"),
    path("notifications/read-all/", views.notificationsReadAll, name="notifications read all"),
]
