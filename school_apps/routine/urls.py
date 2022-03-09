from django.urls import path
from school_apps.routine.views import *
from student_management_system.views import routine_home


app_name = 'routine'

urlpatterns = [
         #for routine
      path('add_routine/', add_routine, name="add_routine"),
      path('manage_routine/', manage_routine, name="manage_routine"),
      path('edit_routine/<str:routine_id>/', edit_routine, name="edit_routine"),
      path('delete_routine/<str:routine_id>/', delete_routine, name="delete_routine"),
      path('routine/view/', view_student_routine, name="view_routine"),
      path('routine-management/', routine_home,name = 'routine-management'),
]
