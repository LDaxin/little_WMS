from django.urls import path

from . import views


urlpatterns = [
    path("accounts/login/", views.loginView, name="login"),
    path("my-data/", views.myData, name="my data"),
    path("users/<int:userId>/delete/", views.deleteUser, name="delete user"),
]
