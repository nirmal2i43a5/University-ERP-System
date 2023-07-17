from django.urls import path
from . import views
from school_apps.administrator.log_views import (
    complain_log,
    delete_complain_log,
    certificate_log,
    delete_certificate_log,
    all_administrator_log,
    delete_all_log,
)

app_name = "administrator"

urlpatterns = [
    path(
        "log/",
        all_administrator_log,
        name="all_administrator_log"),
    path(
        "delete/log/",
        delete_all_log,
        name="delete_all_administrator_log"),
    path(
        "complain/log/",
        complain_log,
        name="complain_log"),
    path(
        "complain/delete/log/",
        delete_complain_log,
        name="delete_complain_log"),
    path(
        "certificate/log/",
        certificate_log,
        name="certificate_log"),
    path(
        "certificate/delete/log/",
        delete_certificate_log,
        name="delete_certificate_log"),
]
