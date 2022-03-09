from django.urls import path
# from student_management_app.views.Admin_views import administrative_views
from school_apps.administrator import views as administrative_views
                                      
from school_apps.student.student_views import views as student_views
from school_apps.teacher.teacher_views import views as teacher_views
from school_apps.parents import views as parent_views
from school_apps.extrausers import views as user_views
from school_apps.announcement import views as announcement_views
from school_apps.academic import views as academic_views
from school_apps.admin_user import views as admin_user_views
from student_management_system.views import (user_home,routine_home,academic_home)


app_name = 'admin_app'

urlpatterns = [

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
      
      
         
      #for syllabus
      path('add_syllabus/', academic_views.add_syllabus, name="add_syllabus"),
      path('manage_syllabus/', academic_views.manage_syllabus, name="manage_syllabus"),
      path('edit_syllabus/<str:syllabus_id>/', academic_views.edit_syllabus, name="edit_syllabus"),
        path('delete_syllabus/<str:syllabus_id>/', academic_views.delete_syllabus, name="delete_syllabus"),
      

      #for assignment
      path('add_assignment/', academic_views.add_assignment, name="add_assignment"),
      path('manage_assignment/', academic_views.manage_assignment, name="manage_assignment"),
       path('student_assignment/', academic_views.student_assignment, name="student_assignment"),
      path('edit_assignment/<str:assignment_id>/', academic_views.edit_assignment, name="edit_assignment"),
      path('delete_assignment/<str:assignment_id>/', academic_views.delete_assignment, name="delete_assignment"),
      
    
      
      #for teacher 
      path('add_teacher/', teacher_views.add_teacher, name="add_staff"),
      path('manage_teacher/', teacher_views.manage_teacher, name="manage_staff"),
      path('edit_teacher/<str:staff_id>/', teacher_views.edit_teacher, name="edit_staff"),
      path('search_teacher/', teacher_views.search_teacher, name="search_staff"),
      path('delete_teacher/<str:staff_id>/', teacher_views.delete_teacher, name="delete_staff"),
      
      # #for view_staff and  staff_file_view 
      path('view_teacher/<str:teacher_id>/', teacher_views.view_teacher, name="view_teacher"),
      path('add_teacher_document/<str:teacher_id>/', teacher_views.add_teacher_document, name="add_teacher_document"),
      path('edit_teacher_document/', teacher_views.edit_teacher_document, name="edit_teacher_document"),
      path('delete_teacher_document/<str:teacher_id>/<str:document_id>/', teacher_views.delete_teacher_document, name="delete_teacher_document"),
      
      #for parent
      path('add_parent/', parent_views.add_parent, name="add_parent"),
      path('manage_parent/', parent_views.manage_parent, name="manage_parent"),
      path('edit_parent/<str:parent_id>/', parent_views.edit_parent, name="edit_parent"),
       path('delete_parent/<str:parent_id>/', parent_views.delete_parent, name="delete_parent"),
      
      #for view_parent 
      path('view_parent/<str:parent_id>/', parent_views.view_parent, name="view_parent"),
      path('add_parent_document/<str:parent_id>/', parent_views.add_parent_document, name="add_parent_document"),
      path('edit_parent_document/', parent_views.edit_parent_document, name="edit_parent_document"),
      path('delete_parent_document/<str:parent_id>/<str:document_id>/', parent_views.delete_parent_document, name="delete_parent_document"),
     
      #for user like driver,receptionist------ 
      path('add_user/', user_views.add_user, name="add_user"),
      path('manage_user/', user_views.manage_user, name="manage_user"),
      path('edit_user/<str:user_id>/', user_views.edit_user, name="edit_user"),
       path('delete_user/<str:user_id>/', user_views.delete_user, name="delete_user"),
      
      
      #for view_user
      path('view_extrauser/<str:extrauser_id>/', user_views.view_extrauser, name="view_extrauser"),
      path('add_extrauser_document/<str:extrauser_id>/', user_views.add_extrauser_document, name="add_extrauser_document"),
      path('edit_extrauser_document/', user_views.edit_extrauser_document, name="edit_extrauser_document"),
      path('delete_extrauser_document/<str:extrauser_id>/<str:document_id>/', user_views.delete_extrauser_document, name="delete_extrauser_document"),
     
      #for student
      path('add_student/', student_views.add_student, name="add_student"),
      path('student_file_upload/', student_views.student_file_upload, name="student_file_upload"),
            path('student_id_card/<str:pk>/', student_views.student_id_card, name="student_id_card"),
      path('manage_student/', student_views.manage_student, name="manage_student"),
      path('edit_student/<str:student_id>/', student_views.edit_student, name="edit_student"),
      path('delete_student/<pk>/', student_views.delete_student, name="delete_student"),
      path('attendance_view/', student_views.attendance_view, name="attendance_view"),
      
      #for view_student and student_file_view 
      path('view_student/<str:student_id>/', student_views.view_student, name="view_student"),
      path('add_student_document/<str:student_id>/', student_views.add_student_document, name="add_student_document"),
      # path('edit_student_document/<str:student_id>/<str:document_id>/', student_views.edit_student_document, name="edit_student_document"),
      path('edit_student_document/', student_views.edit_student_document, name="edit_student_document"),
      path('delete_student_document/<str:student_id>/<str:document_id>/', student_views.delete_student_document, name="delete_student_document"),
   
     
      
     
      

      
      
      #for session year
      path('add_manage_session/', administrative_views.add_manage_session_year, name="add_manage_session"),
      path('edit_session/<str:session_id>/', administrative_views.edit_session, name="edit_session"),
       path('delete_session/<str:session_id>/', administrative_views.delete_session, name="delete_session"),
      
      #for student group
      path('manage_studentgroup/', administrative_views.add_manage_group, name="add_manage_group"),
      path('edit_studentgroup/<str:group_id>/', administrative_views.edit_group, name="edit_group"),
      path('delete_studentgroup/<str:group_id>/', administrative_views.delete_group, name="delete_group"),
      

    
     
    
         path('add_sociallink/', administrative_views.add_sociallink, name="add_sociallink"),
      path('manage_sociallink/', administrative_views.manage_sociallink, name="manage_sociallink"),
      path('edit_sociallink/<str:sociallink_id>/', administrative_views.edit_sociallink, name="edit_sociallink"),
      path('delete_sociallink/<str:sociallink_id>/', administrative_views.delete_sociallink, name="delete_sociallink"),
    
        #for certificate template
        path('add_certificate_template/', administrative_views.add_certificate_template, name="add_certificate_template"),
      path('edit_certificate_template/<str:certificate_template_id>/', administrative_views.edit_certificate_template, name="edit_certificate_template"),
      path('manage_certificate_template/', administrative_views.manage_certificate_template, name="manage_certificate_template"),
      path('delete_certificate_template/<str:certificate_template_id>/', administrative_views.delete_certificate_template, name="delete_certificate_template"),
    
      path('print_character_certificate/<str:certificate_id>/<str:student_id>/', administrative_views.print_character_certificate, name="print_character_certificate"),
    
    #for admin
      path('add_system_admin/', admin_user_views.add_admin, name="add_system_admin"),
      path('manage_system_admin/', admin_user_views.manage_system_admin, name="manage_system_admin"),
      path('edit_system_admin/<str:admin_id>/', admin_user_views.edit_system_admin, name="edit_system_admin"),
    
     path('delete_system_admin/<str:admin_id>/', admin_user_views.delete_system_admin, name="delete_system_admin"),
    
    
    # Sidebar module manage
    path('user-management/', user_home,name = 'user-management'),
      path('academic-management/',academic_home,name = 'academic-management'),
]