from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r"^tag/(?P<tagId>[0-9]+)/update", views.updateTag, name="update Tag"),
    re_path(r'^tag/(?P<tagId>[0-9]+)/i', views.tagIncert, name="Tag"),
    re_path(r'^tag/(?P<tagId>[0-9]+)', views.tag, name="Tag"),
    re_path(r"^tag/add", views.addTag, name="add Tag"),
    re_path(r"^tag/del", views.delTag, name="del Tag"),
    re_path(r"^tag/", views.tags, name="Tags"),
]

