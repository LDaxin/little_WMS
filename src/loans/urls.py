from django.urls import path

from . import views


urlpatterns = [
    path("lendings/", views.lendings, name="lendings"),
    path("lendings/<int:lendingId>/return/", views.returnLending, name="return lending"),
    path("article/<str:typ>/<int:articleId>/lend", views.lendArticle, name="lend article"),
    path("loans/", views.loans, name="loans"),
    path("loans/<int:loanId>/return/", views.returnLoan, name="return loan"),
    path("article/<str:typ>/<int:articleId>/borrow", views.borrowArticle, name="borrow article"),
]
