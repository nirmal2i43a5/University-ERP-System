from django.urls import path
from .views import (
    UserRoleCreate,
    UserRoleUpdate,
    # UserRoleMange,
    UserPermissionCreate,
    user_permission_manage,
    save_permission,manage_role
)
from student_management_system.views import permission_home

app_name = "role_app"

urlpatterns = [
    path("add_role/", UserRoleCreate.as_view(), name="add_role"),
    path("edit_role/<str:pk>/", UserRoleUpdate.as_view(), name="edit_role"),
    path("manage_role/", manage_role, name="manage_role"),
    path(
        "add_permission/",
        UserPermissionCreate.as_view(),
        name="add_permission"),
    # path('edit_permission/<str:pk>/',UserRoleUpdate.as_view(),name = 'edit_permission'),
    path(
        "manage_permission/",
        user_permission_manage,
        name="manage_permission"),
    path("save_permission/", save_permission, name="save_permission"),
    # path(
    #     "permission-management/", UserRoleMange.as_view(), name="permission-management"
    # ),
]
