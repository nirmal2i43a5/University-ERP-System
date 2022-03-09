from django.urls import path
from school_apps.academic.log_views import * 
from school_apps.academic.views import (assignment_answer_upload,student_assignment_grade,
                                        assignment_retured,draft_publish_unpublish,add_assignment_grade,
                                            manage_coursecategory,view_student_syllabus)
# from student_management_system.views import academic_home
app_name = 'academic'


urlpatterns = [
    path('assignment/answer/<str:assignment_id>/<str:student_id>/', assignment_answer_upload, name = 'assignment_answer_upload'),
    path('student/assignments/<str:assignment_id>/',student_assignment_grade,name = 'student_assignment_grade'),
    path('add_assignment_grade/<str:pk>/',add_assignment_grade,name = 'add_assignment_grade'),
    path('draft_publish_unpublish/<str:pk>/',draft_publish_unpublish,name = 'draft_publish_unpublish'),
    path('assignment_retured/',assignment_retured,name = 'assignment_retured'),
    path('manage_coursecategory/', manage_coursecategory, name="manage_coursecategory"),
    path('syllabus/view/', view_student_syllabus, name="view_syllabus"),
    
    path('log/',academic_logs,name = 'academic_log'),
    path('assignment/log/',assignment_log,name = 'assignment_log'),
    path('routine/log/',routine_log,name = 'routine_log'),
    path('section/log/',section_log,name = 'section_log'),
    path('semester/log/',semester_log,name = 'semester_log'),
    path('subject/log/',subject_log,name = 'subject_log'),
    path('syllabus/log/',syllabus_log,name = 'syllabus_log'),
    
    
    
    # ---------------------------------------
    
    # Dynamic sidebar manage
    
]
