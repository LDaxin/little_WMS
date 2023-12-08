from django.urls import path, re_path
from . import views


urlpatterns = [
    #views.updatecode, name="update code"),
    #re_path(r'^code/(?P<codeId>[0-9]+)/i', views.codeIncert, name="code"),
    #re_path(r'^code/(?P<codeId>[0-9]+)', views.code, name="code"),
    re_path(r"^code/add", views.addCode, name="add code"),
    re_path(r"^code/add/modal", views.addModal, name="add code Modal"),
    #re_path(r"^code/del", views.delcode, name="del code"),
    #re_path(r"^code/upadte", views.delcode, name="del code"),
    re_path(r"^code/search", views.searchCodes, name="search"),
    re_path(r"^code/", views.codes, name="codes"),
]
