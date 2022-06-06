from django.urls import path
from student_management_app.views import TeacherViews


app_name = 'teacher_app'

urlpatterns = [
      
      path('teacher_home/', TeacherViews.teacher_home, name ="teacher_home"),
      
    
      
      
    
]