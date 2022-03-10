
    
    
from django.urls import path
from school_apps.routine.views import *
from student_management_system.views import log_history_home
from school_apps.log_history.views import user_log_list

    
app_name = 'user_history'

urlpatterns = [
         #for routine
        path('user/logs/',user_log_list,name="user_log"),
 
]
