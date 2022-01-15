from django.urls import path
from school_apps.attendance.views import (get_students, save_student_attendance, manage_student_attendance,
                              get_teachers,save_teacher_attendance, manage_teacher_attendance,
                              get_users, save_user_attendance, manage_user_attendance ,
                              edit_student_attendance,edit_save_student_attendance,
                              student_attendance_list,fill_semester_select,fill_section_select,
                              fill_subject_select,student_attendance_report,student_daily_attendance,student_monthly_attendance
                              )

app_name = 'attendance_app'

urlpatterns = [
    
    path('student_attendance/',get_students,name = 'student_attendance'),
    path('save_student_attendance/',save_student_attendance,name = 'save_student_attendance'),
    path('manage_student_attendance/',manage_student_attendance,name = 'manage_student_attendance'),
    path('student_attendance_list/',student_attendance_list,name = 'student_attendance_list'),
    path('edit_student_attendance/',edit_student_attendance,name = 'edit_student_attendance'),
    path('edit_save_student_attendance/',edit_save_student_attendance,name = 'edit_save_student_attendance'),
 
    path('teacher_attendance/',get_teachers,name = 'teacher_attendance'),
    path('save_teacher_attendance/',save_teacher_attendance,name = 'save_teacher_attendance'),
    path('manage_teacher_attendance/',manage_teacher_attendance,name = 'manage_teacher_attendance'),
    
        path('student_attendance_report/',student_attendance_report,name = 'student_attendance_report'),
        path('student_monthly_attendance/',student_monthly_attendance,name = 'student_monthly_attendance'),
        path('student_daily_attendance/',student_daily_attendance,name = 'student_daily_attendance'),
        
    path('user_attendance/',get_users,name = 'user_attendance'),
    path('save_user_attendance/',save_user_attendance,name = 'save_user_attendance'),
    path('manage_user_attendance/',manage_user_attendance,name = 'manage_user_attendance'),
    # for auto fill form part
    path('fill_semester_select/',fill_semester_select,name = 'fill_semester_select'),
     path('fill_section_select/',fill_section_select,name = 'fill_section_select'),
        path('fill_subject_select/',fill_subject_select,name = 'fill_subject_select'),
    
 

]