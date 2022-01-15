from django.urls import path
from . import views
from school_apps.student.student_views.views import *

app_name = 'student'

urlpatterns=[
    path('home/', views.index, name='index'),
    path('checkscore/', views.checkscore, name='checkscore'),
    path('selectcourse/', views.selectcourse, name='addcourse'),
    path('registerexam/', views.registerexam, name='registerexam'),
    path('examapplication/', views.examapplication, name='examapplication'),
    path('examdetails/', views.examdetails, name='examdetails'),
    path('viewcourses/', views.viewcourses, name='viewcourses'),
    path('viewform/', views.viewform, name='viewform'),
    path('print_results/<str:form_id>/', views.printresults, name='printresults'),
    path('print_admitcard/', views.printadmitcard, name='printadmitcard'),
    path('printapplicationform/', views.printapplicationform, name='printapplicationform'),
    path('student_application/', views.student_application, name='student_application'),
    # path('show_routine/', views.show_routine, name='show_routine'),
    path('ajax/examslist/', views.examslist, name = "examslist"),
    path('ajax/testexamAjax/', views.testexamAjax, name = "testexamAjax"),
    path('ajax/confirmexamAjax/', views.confirmexamAjax, name = "confirmexamAjax"),
    path('ajax/courses/', views.postCourses, name = "postCourses"),
    path('ajax/grades/', views.postGrades, name = "postGrades"),
    path('ajax/exams/', views.postExams, name = "postExams"),
    path('ajax/addcourse/', views.addAjax, name = "addAjax"),
    path('ajax/confirmcourse/', views.confirmAjax, name = "confirmAjax"),
    path('student/log/', student_log, name = "student_log"),
    path('student/delete/log/', delete_log, name = "delete_log"),
    path('student/attendance/<student_id>/', student_attendance_view, name='student_attendance_view'),
    path('check_email_exists/',views.check_email_exist,name='check_email_exist'),
    path('bulkprintidcard/',bulk_print_id_card,name='bulk_print_id_card'),

    #``````````````````````````````````````````````````````````````````````````````````````````````#
    #parent#
    path('parent/checkscore/', views.parent_checkscore, name='parent_checkscore'),
    path('ajax/returnExamslist/', views.returnExamslist, name = "returnExamslist"),
    path('student_autocomplete/', views.student_ajax_autocomplete, name = "student_ajax_autocomplete"),
    path('student_bulk_photo_upload/', student_bulk_photo_upload, name = "student_bulk_photo_upload"),
      path('make_student_inactive/<pk>/', make_student_inactive, name = "make_student_inactive"),
         path('restore_inactive_student/<pk>/', restore_inactive_students, name = "restore_inactive_students"),
        path('inactive_students/', inactive_students, name = "inactive_students"),
    
    
]