from django.urls import path
from school_apps.transports.views import *
from student_management_system.views import transport_home


app_name = "transport"

urlpatterns = [
    # for transport
    path("add_transport/", add_transport, name="add_transport"),
    path("manage_transport/", manage_transport, name="manage_transport"),
    path("edit_transport/<str:transport_id>/",
         edit_transport, name="edit_transport"),
    path(
        "delete_transport/<str:transport_id>/",
        delete_transport,
        name="delete_transport",
    ),
    path("transport_member/", transport_member, name="transport_member"),
    path("transport-management/", transport_home, name="transport-management"),
]
