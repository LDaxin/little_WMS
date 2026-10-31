from django.urls import path

from . import views


urlpatterns = [
    path("loans/", views.loans, name="loans"),
    path("loans/<int:loanId>/return/", views.returnLoan, name="return loan"),
    path("article/<str:typ>/<int:articleId>/lend", views.lendArticle, name="lend article"),
]
