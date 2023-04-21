from django.urls import path
from . import views

from school_apps.teacher.teacher_views.views import *
app_name = 'teacher'

urlpatterns=[
    # path('home', views.index, name='index'),
    path('addscore/', views.addscore, name='addscore'),
    path('addscore/code', views.subscore, name='subscore'),
    path('submitscore/', views.submitscore, name='submitscore'),
    path('submitscore/edit/', views.editsubmitscore, name='edit_submitscore'),

    path('checksubjects/', views.checksubjects, name='checksubjects'),
    path('checkstudents/', views.checkstudents, name='checkstudents'),
    path('checkscore/', views.checkscore, name='checkscore'),
    path('login', views.login, name = "login"),
    path('uploadcsv', views.uploadcsv, name = "uploadcsv"),
    # path('logout', views.logout, name = "logout"),
    path('exportcsv/<str:exam_id>', views.exportcsv, name = "exportcsv"),
    path('studentlist/', views.studentlist, name='studentlist'),
    path('ajax/studentlist', views.examsAjax, name='examsAjax'),
    path('ajax/loadExamsAjax', views.loadExamsAjax, name='loadExamsAjax'),
    path('teacher/log/', teacher_log, name = "teacher_log"),
    path('teacher/delete/log/', delete_log, name = "delete_log"),
    path('teacher/students/', student_view_by_teacher, name='student_view_by_teacher'),
    path('attendance/home/', teacher_attendance_home, name='teacher_attendance_home'),

    # path('attendance/<student_id>/', attendance_view_by_parent, name='attendance_view_by_parent'),
]