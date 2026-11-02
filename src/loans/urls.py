from django.urls import path

from . import views


urlpatterns = [
    path("loans/", views.loans, name="loans"),
    path("loans/<int:loanId>/return/", views.returnLoan, name="return loan"),
    path("loans/<int:loanId>/confirm/", views.confirmLoan, name="confirm loan"),
    path("lend-links/", views.lendLinks, name="lend links"),
    path("lend-links/<int:linkId>/revoke/", views.lendLinkRevoke, name="revoke lend link"),
    path("lend/<str:token>/", views.lendLinkView, name="lend link"),
    path("article/<str:typ>/<int:articleId>/lend", views.lendArticle, name="lend article"),
    path("article/<str:typ>/<int:articleId>/borrow", views.borrowArticle, name="borrow article"),
]
