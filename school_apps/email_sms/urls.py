from django.urls import path
from .views import *
from student_management_system.views import email_services_home

app_name = 'email_sms'

urlpatterns = [
    path('send_message_student/', student_send_bulk_email, name="student_send_bulk_email"),
    path('send_message_teacher/', teacher_send_bulk_email, name="teacher_send_bulk_email"),
    path('send_message_user/', particular_user_email, name="user_send_bulk_email"),
    path('send_sms/', send_sms, name="send_sms"),
    path('send_sms_ajax', send_sms_ajax, name='send_sms_ajax'),
    path('email-sms-management/', email_services_home,name = 'email-sms-management'),#for dynamic sidebar
]
