from django.urls import path
from . import views
from school_apps.extrausers.views import extrauser_log,delete_log

app_name = 'extrauser'

urlpatterns=[

    path('log/', extrauser_log, name = "user_log"),
    path('delete/log/', delete_log, name = "delete_log"),

]