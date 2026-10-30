from django.urls import path

from . import views


urlpatterns = [
    path("roles/", views.roles, name="roles"),
    path("roles/create/", views.roleCreate, name="role create"),
    path("roles/<int:roleId>/", views.roleDetail, name="role detail"),
    path("roles/<int:roleId>/save/", views.roleSave, name="role save"),
    path("roles/<int:roleId>/delete/", views.roleDelete, name="role delete"),
    path("users/", views.users, name="users"),
    path("users/<int:userId>/role/", views.userRole, name="user role"),
    path("select-organisation/", views.selectOrganisation, name="select organisation"),
    path("switch-organisation/", views.switchOrganisation, name="switch organisation"),
    path("invitations/create/", views.inviteCreate, name="invite create"),
    path("invitations/<int:invitationId>/revoke/", views.inviteRevoke, name="invite revoke"),
    path("invite/<str:token>/", views.inviteAccept, name="invite accept"),
]
