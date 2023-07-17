from django.urls import path
from . import views
from student_management_system.views import exam_home

app_name = 'courses'

urlpatterns=[
  
    path('addexam/', views.addexam, name='addexam'),
    path('addterm/', views.addterm, name='addterm'),
    path('ajax/addexam_marks_ajax/', views.addexam_marks_ajax, name='addexam_marks_ajax'),
    path('viewterm/', views.viewterm, name='viewterm'),
    path('checkterm_exams/<str:pk>/', views.checkterm_exams, name='checkterm_exams'),
    path('results-each-subjects/', views.get_result_of_each_subject, name='get_result_of_each_subject'),
    path('results-all-subjects/', views.get_results_of_all_subjects, name='get_results_of_all_subjects'),
    path('student/get_result/', views.get_results_of_all_subjects, name='get_result_by_student'),


    path('publishresults/', views.publishresults, name='publishresults'),
    path('toggle_results/<str:pk>/', views.toggle_results, name="toggle_results"),
    path('examreport/', views.examreport, name='examreport'),
    path('viewresults/', views.viewresults, name='viewresults'),
    path('examtoppers/', views.examtoppers, name='examtoppers'),
    path('addstudentmarks/', views.addstudentmarks, name='addstudentmarks'),
    path('submitscores/', views.submitscores, name='submitscores'),
    

    #bulk print admit cards
    path('bulkprintadmitcard/', views.bulkprintadmitcard, name='bulkprintadmitcard'),
    path('printadmitcards/', views.printadmitcards, name='printadmitcards'),
    path('ajax/returnexamdropdown/', views.returnexamdropdown, name='returnexamdropdown'),
    path('ajax/return_exams_admit/', views.return_exams_admit, name='return_exams_admit'),
    path('ajax/returnstudentlist_admit/', views.returnstudentlist_admit, name='returnstudentlist_admit'),

    #bulk print results
    path('bulkprintresults/', views.bulkprintresults, name='bulkprintresults'),
    path('ajax/return_exams_results/', views.return_exams_results, name='return_exams_results'),
    path('ajax/returnstudentlist_results/', views.returnstudentlist_results, name='returnstudentlist_results'),
    path('printresults/', views.printresults, name='printresults'),

    path('confirmexamapplication/', views.confirmexamapplication, name='confirmexamapplication'),
    path('studentmarksentry/<str:id>', views.studentsmarksentry, name='studentmarksentry'),
    path('confirmapplication/', views.confirmapplication, name='confirmapplication'),
    path('ajax/studentlist/', views.studentsAjax, name='studentlist'),
    path('ajax/confirmAjax/', views.confirmAjax, name='confirmAjax'),

    path('ajax/returnexamlist/', views.returnexamlist_Ajax, name='returnexamlist_ajax'),
    path('printexamreport/<str:pk>', views.printexamreport, name='printexamreport'),
    path('ajax/fill_section_select/', views.fill_section_select, name='fill_section_select'),

    #add exam marks
    path('addexammarks/', views.addexammarks, name='addexammarks'),
    path('addremarks/', views.addremarks, name='addremarks'),
    path('editremarks/<str:pk>', views.editremarks, name='editremarks'),
    path('addstudentremarks/<str:term_id>/<str:student_id>',views.addstudentremarks, name='addstudentremarks'),
    path('ajax/fill_exam_select/', views.fill_exam_select, name='fill_exam_select'),
    path('ajax/examsAjax/', views.examsAjax, name='examsAjax'),

    #mass exam application
    path('massexamapplication', views.massexamapplication, name="massexamapplication"),
    path('toggle_application/<str:pk>', views.toggle_application, name="toggle_application"),
    path('printresults/', views.gci_printresults, name="gci_printresults"),


   path('exam-management/',exam_home ,name = 'exam-management'),

    
    
    
]