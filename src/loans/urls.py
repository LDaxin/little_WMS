from django.urls import path

from . import views


urlpatterns = [
    path("lendings/", views.lendings, name="lendings"),
    path("lendings/<int:lendingId>/return/", views.returnLending, name="return lending"),
    path("article/<str:typ>/<int:articleId>/lend", views.lendArticle, name="lend article"),
    path("loans/", views.loans, name="loans"),
    path("loans/<int:loanId>/return/", views.returnLoan, name="return loan"),
    path("loans/<int:loanId>/confirm/", views.confirmLoan, name="confirm loan"),
    path("loan-offers/", views.loanOffers, name="loan offers"),
    path("loan-offers/create/", views.createLoanOffer, name="create loan offer"),
    path("loan-offers/<int:offerId>/borrow/", views.borrowFromOffer, name="borrow from offer"),
    path("article/<str:typ>/<int:articleId>/borrow", views.borrowArticle, name="borrow article"),
]
