
    
    
from django.urls import path
from school_apps.routine.views import *
from student_management_system.views import log_history_home
from school_apps.log_history.views import user_log_list,academic_log,attendance_log,announcement_log

    
app_name = 'user_history'

urlpatterns = [
         #for routine
        path('user/logs/',user_log_list,name="user_log"),
         path('log-history-management/',log_history_home,name="log-history-management"),
         path('academic-log/',academic_log,name="academic-log"),
             path('attendance-log/',attendance_log,name="attendance-log"),
                 path('announcement-log/',announcement_log,name="announcement-log"),
 
]
