from django.urls import path
from . import views
from school_apps.announcement.log_views import (notice_log,delete_notice_log,event_log, delete_event_log, all_announcement_log,delete_all_log)
from school_apps.announcement.views import *
from student_management_system.views import announcement_home

app_name = 'announcement'

urlpatterns=[
    
    path('add_notice/', add_notice, name="add_notice"),
    path('ajax/update_notice/', update_notice, name="update_notice"),
    path('manage_notice/', manage_notice, name="manage_notice"),
    path('edit_notice/<str:notice_id>/', edit_notice, name="edit_notice"),
    path('delete_notice/<str:notice_id>/', delete_notice, name="delete_notice"),
    path('add_holiday/', add_holiday, name="add_holiday"),
    path('manage_holiday/', manage_holiday, name="manage_holiday"),
    path('edit_holiday/<str:holiday_id>/', edit_holiday, name="edit_holiday"),
    path('delete_holiday/<str:holiday_id>/', delete_holiday, name="delete_holiday"),
    path('log/', all_announcement_log, name = "all_announcement_log"),
    path('delete/log/', delete_all_log, name = "delete_all_announcement_log"),
    path('notice/log/', notice_log, name = "notice_log"),
    path('notice/delete/log/', delete_notice_log, name = "delete_notice_log"),
    path('event/log/', event_log, name = "event_log"),
    path('event/delete/log/', delete_event_log, name = "delete_event_log"),
    
    path('announcement-management/', manage_notice,name = 'announcement-management'),#for dynamic sidebar

]