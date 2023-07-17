from django.urls import path
from school_apps.notifications.views import (
    show_notification,
    update_notification,
    delete_notification,
    notification_detail,
)

app_name = "notifications"
urlpatterns = [
    path("", show_notification, name="show-notifications"),
    path("update/", update_notification, name="update_notification"),
    path("detail/<str:pk>/", notification_detail, name="notification_detail"),
    path("delete/", delete_notification, name="delete_notification"),
]
