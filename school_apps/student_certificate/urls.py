from django.urls import path
from school_apps.student_certificate.views import *
from student_management_system.views import certificate_home


app_name = 'certificate'

urlpatterns = [
       #for certificate template
      path('create_certificate_template/', add_certificate_template, name="add_certificate_template"),
      path('edit_certificate_template/<str:certificate_template_id>/', edit_certificate_template, name="edit_certificate_template"),
      path('manage_certificate_template/', manage_certificate_template, name="manage_certificate_template"),
      path('delete_certificate_template/<str:certificate_template_id>/', delete_certificate_template, name="delete_certificate_template"),
    
      path('print_character_certificate/<str:certificate_id>/<str:student_id>/', print_character_certificate, name="print_character_certificate"),

    path('certificate-management/', certificate_home,name = 'certificate-management'),
]
