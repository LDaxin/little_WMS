from django.urls import path

from . import views


urlpatterns = [
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/<int:notificationId>/read/", views.notificationRead, name="notification read"),
    path("notifications/read-all/", views.notificationsReadAll, name="notifications read all"),
    path("notifications/rules/", views.rules, name="notification rules"),
    path("notifications/rules/add/", views.ruleAdd, name="notification rule add"),
    path("notifications/rules/<int:ruleId>/", views.ruleEdit, name="notification rule edit"),
    path("notifications/rules/<int:ruleId>/delete/", views.ruleDelete, name="notification rule delete"),
]
