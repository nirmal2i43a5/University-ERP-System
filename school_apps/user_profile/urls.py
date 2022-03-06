from django.urls import path
from .views import *
# from .views import (loginView,logoutView,user_change_password,UpdateStudentProfile, 
#                     UpdateTeacherProfile, UpdateAdminProfile, student_send_bulk_email,
#                     teacher_send_bulk_email, particular_user_email,UpdateParentProfile,change_other_password,a_level_home)

urlpatterns = [
    path('accounts/login/',loginView,name = "login"),
    path('logout/',logoutView,name = "logout"),
 
    path('user_password_reset/', user_change_password, name="change_password"),
    path('change_other_password/', change_other_password, name="change_other_password"),
    path('student_profile_update/', UpdateStudentProfile, name="student_profile_update"),
    path('teacher_profile_update/', UpdateTeacherProfile, name="teacher_profile_update"),
    path('parent_profile_update/', UpdateParentProfile, name="parent_profile_update"),
    path('profile_update/', UpdateAdminProfile, name="admin_profile_update"),
    path('send_message_student/', student_send_bulk_email, name="student_send_bulk_email"),
    path('send_message_teacher/', teacher_send_bulk_email, name="teacher_send_bulk_email"),
    path('send_message_user/', particular_user_email, name="user_send_bulk_email"),
    path('send_sms/', send_sms, name="send_sms"),
    path('send_sms_ajax', send_sms_ajax, name='send_sms_ajax')
]
