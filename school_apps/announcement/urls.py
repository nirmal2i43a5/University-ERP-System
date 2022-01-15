from django.urls import path
from . import views
from school_apps.announcement.log_views import (notice_log,delete_notice_log,event_log, delete_event_log, all_announcement_log,delete_all_log)

app_name = 'announcement'

urlpatterns=[
   path('log/', all_announcement_log, name = "all_announcement_log"),
    path('delete/log/', delete_all_log, name = "delete_all_announcement_log"),
    path('notice/log/', notice_log, name = "notice_log"),
    path('notice/delete/log/', delete_notice_log, name = "delete_notice_log"),
    path('event/log/', event_log, name = "event_log"),
    path('event/delete/log/', delete_event_log, name = "delete_event_log"),

]