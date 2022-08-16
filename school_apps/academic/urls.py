from django.urls import path
from school_apps.academic.log_views import * 
from school_apps.academic.views import (assignment_answer_upload,student_assignment_grade,
                                        assignment_retured,draft_publish_unpublish,add_assignment_grade,edit_assignment_grade,assignment_returned_update,
                                            manage_coursecategory,view_student_syllabus,add_enotes,edit_enotes,manage_enotes,delete_enote)
from student_management_system.views import academic_home
from school_apps.academic import views as academic_views
from school_apps.routine.views import *

app_name = 'academic'


urlpatterns = [
    path('assignment/answer/<str:assignment_id>/', assignment_answer_upload, name = 'assignment_answer_upload'),
    path('student/assignments/<str:assignment_id>/',student_assignment_grade,name = 'student_assignment_grade'),
    path('add_assignment_grade/<str:pk>/<str:student_id>/',add_assignment_grade,name = 'add_assignment_grade'),
    path('edit_assignment_grade/<str:pk>/<str:student_id>/',edit_assignment_grade,name = 'edit_assignment_grade'),
    
    path('draft_publish_unpublish/<str:pk>/',draft_publish_unpublish,name = 'draft_publish_unpublish'),
    path('assignment_retured/',assignment_retured,name = 'assignment_retured'),
     path('assignment_returned_update/',assignment_returned_update,name = 'assignment_returned_update'),
    path('manage_coursecategory/', manage_coursecategory, name="manage_coursecategory"),
    path('syllabus/view/', view_student_syllabus, name="view_syllabus"),
       #for course
    path('add_manage_course/', academic_views.add_manage_course, name="add_manage_course"),
    path('add_department/', academic_views.add_department, name="add_department"),
          path('edit_department/<str:pk>/', academic_views.edit_department, name="edit_department"),
               path('delete_department/<str:pk>/', academic_views.delete_department, name="delete_department"),
      path('edit_course/<str:course_id>/', academic_views.edit_course, name="edit_course"),
      path('save_edit_course/', academic_views.save_edit_course, name="save_edit_course"),
      path('delete_course/<str:course_id>/', academic_views.delete_course, name="delete_course"),
      
            
      #for class
      path('manage_class/', academic_views.manage_class, name="manage_class"),
      # path('manage_class/', academic_views.manage_class, name="manage_class"),
      path('edit_class/<str:class_id>/', academic_views.edit_class, name="edit_class"),
      path('delete_class/<str:class_id>/', academic_views.delete_class, name="delete_class"),
      
      #for section  
      path('manage_section/', academic_views.manage_section, name="manage_section"),
      path('edit_section/<str:section_id>/', academic_views.edit_section, name="edit_section"),
       path('delete_section/<str:section_id>/', academic_views.delete_section, name="delete_section"),
      
      #for subject
      path('manage_subject/', academic_views.manage_subject, name="manage_subject"),
      path('edit_subject/<str:subject_id>/', academic_views.edit_subject, name="edit_subject"),
      path('search_subject/', academic_views.search_subject, name="search_subject"),
      path('delete_subject/<str:subject_id>/', academic_views.delete_subject, name="delete_subject"),
      #subject to teacher
    path('assign_subject_to_teacher/', academic_views.assign_subject_to_teacher, name='assign_subject_to_teacher'),
      path('assign_class_to_teacher/', academic_views.assign_class_to_teacher, name='assign_class_to_teacher'),
    path('manage_subject_teacher/', academic_views.showsubjectteacherlist, name='showsubjectteacherlist'),
        path('ajax/class_to_teacher/', academic_views.class_to_teacher_Ajax, name='class_to_teacher_ajax'),
           path('manage_class_teacher/', academic_views.manage_class_teacher, name='manage_class_teacher'),
    path('edit_subject_teacher/', academic_views.editsubjectteacher, name='editsubjectteacher'),      #<str:exam_id>
    path('delete_subjectteacher/<str:pk>/', academic_views.deletesubjectteacher, name='deletesubjectteacher'),
    path('ajax/subject_to_teacher/', academic_views.subject_to_teacher_Ajax, name='subject_to_teacher_ajax'),

    #subject to class
    path('subject_to_class/', academic_views.subject_to_class, name='subject_to_class'),
    path('ajax/subject_to_class/', academic_views.subject_to_class_Ajax, name='subject_to_class_ajax'),
  

    #subject to student
    path('assign_subject_to_student/', academic_views.assign_subject_to_student, name='assign_subject_to_student'),
    path('drop_subject/', academic_views.drop_subject, name='drop_subject'),
    path('ajax/subject_to_student/', academic_views.subject_to_student_Ajax, name='subject_to_student_ajax'),
    path('ajax/return_student_subject/', academic_views.return_student_subject, name='return_student_subject'),
    path('delete_subjectstudent/<str:pk>/', academic_views.deletesubjectstudent, name='deletesubjectstudent'),
    path('studentdetails/', academic_views.student_details, name='student_details'),
    
         
      #for syllabus
      path('add_syllabus/', academic_views.add_syllabus, name="add_syllabus"),
      path('manage_syllabus/', academic_views.manage_syllabus, name="manage_syllabus"),
      path('edit_syllabus/<str:syllabus_id>/', academic_views.edit_syllabus, name="edit_syllabus"),
        path('delete_syllabus/<str:syllabus_id>/', academic_views.delete_syllabus, name="delete_syllabus"),
      # routine
      
            path('add_routine/', add_routine, name="add_routine"),
      path('manage_routine/', manage_routine, name="manage_routine"),
      path('edit_routine/<str:routine_id>/', edit_routine, name="edit_routine"),
      path('delete_routine/<str:routine_id>/', delete_routine, name="delete_routine"),
      path('routine/view/', view_student_routine, name="view_routine"),
# e-notes
   path('add_enotes/', academic_views.add_enotes, name="add_enote"),
      path('edit_enotes/<str:pk>/', academic_views.edit_enotes, name="edit_enote"),
       path('enotes/', academic_views.manage_enotes, name="manage_enote"),
           path('delete_enote/<str:pk>/', delete_enote, name="delete_enote"),
      #for assignment
      path('add_assignment/', academic_views.add_assignment, name="add_assignment"),
      path('manage_assignment/', academic_views.manage_assignment, name="manage_assignment"),
       path('student_assignment/', academic_views.student_assignment, name="student_assignment"),
      path('edit_assignment/<str:assignment_id>/', academic_views.edit_assignment, name="edit_assignment"),
      path('delete_assignment/<str:assignment_id>/', academic_views.delete_assignment, name="delete_assignment"),
      
    path('log/',academic_logs,name = 'academic_log'),
    path('assignment/log/',assignment_log,name = 'assignment_log'),
    path('routine/log/',routine_log,name = 'routine_log'),
    path('section/log/',section_log,name = 'section_log'),
    path('semester/log/',semester_log,name = 'semester_log'),
    path('subject/log/',subject_log,name = 'subject_log'),
    path('syllabus/log/',syllabus_log,name = 'syllabus_log'),
    path('academic-management/',academic_home,name = 'academic-management'),
    
    
    
    
    
    # ---------------------------------------
    
    # Dynamic sidebar manage
    
]
