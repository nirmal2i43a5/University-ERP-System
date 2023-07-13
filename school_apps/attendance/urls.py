from django.urls import path
from school_apps.attendance.views import (get_students, save_student_attendance, manage_student_attendance,
                              get_teachers,save_teacher_attendance, manage_teacher_attendance,
                              get_users, save_user_attendance, manage_user_attendance ,
                              edit_student_attendance,edit_save_student_attendance,
                              student_attendance_list,fill_semester_select,fill_semester_from_course,fill_section_select,fill_course_select,fill_student_select,
                              fill_subject_select,fill_teacher_select,student_attendance_report,student_daily_attendance,student_monthly_attendance
                              )
from student_management_system.views import attendance_home
from school_apps.student.student_views.views import student_attendance_view,student_view_own_attendance,teacher_attendance_view
app_name = 'attendance_app'

urlpatterns = [
    
    path('student_attendance/',get_students,name = 'student_attendance'),
    path('save_student_attendance/',save_student_attendance,name = 'save_student_attendance'),
    path('manage_student_attendance/',manage_student_attendance,name = 'manage_student_attendance'),
    path('fetch_student_attendance/',student_attendance_list,name = 'student_attendance_list'),
    path('edit_student_attendance/',edit_student_attendance,name = 'edit_student_attendance'),
    path('edit_save_student_attendance/',edit_save_student_attendance,name = 'edit_save_student_attendance'),
 
    path('teacher_attendance/',get_teachers,name = 'teacher_attendance'),
         path('teacher/attendance/<teacher_id>/', teacher_attendance_view, name='teacher_attendance_view'),
    path('save_teacher_attendance/',save_teacher_attendance,name = 'save_teacher_attendance'),
    path('manage_teacher_attendance/',manage_teacher_attendance,name = 'manage_teacher_attendance'),
    
        path('student_attendance_report/',student_attendance_report,name = 'student_attendance_report'),
        path('student_monthly_attendance/',student_monthly_attendance,name = 'student_monthly_attendance'),
        path('student_daily_attendance_report/',student_daily_attendance,name = 'student_daily_attendance'),
        
    path('user_attendance/',get_users,name = 'user_attendance'),
    path('save_user_attendance/',save_user_attendance,name = 'save_user_attendance'),
    path('manage_user_attendance/',manage_user_attendance,name = 'manage_user_attendance'),
    # for auto fill form part
      path('fill_course_select/',fill_course_select,name = 'fill_course_select'),
    path('fill_semester_select/',fill_semester_select,name = 'fill_semester_select'),
      path('fill_semester_from_course/',fill_semester_from_course,name = 'fill_semester_from_course'),
     path('fill_section_select/',fill_section_select,name = 'fill_section_select'),
     path('fill_student_select/',fill_student_select,name = 'fill_student_select'),

        path('fill_subject_select/',fill_subject_select,name = 'fill_subject_select'),
          path('fill_teacher_select/',fill_teacher_select,name = 'fill_teacher_select'),
      path('student/attendance/<student_id>/', student_attendance_view, name='student_attendance_view'),
           path('attendance/view/', student_view_own_attendance, name='student_view_own_attendance'),
        
    
 path('attendance-management/', attendance_home,name = 'attendance-management'),

]