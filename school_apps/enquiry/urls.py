from django.urls import path
from . import views

app_name = 'enquiry'

urlpatterns = [
    path('enquiryform/', views.enquiryform, name='enquiryform'),
    path('enquiries/', views.EnquiryListView.as_view(), name='enquiry_list'),
    path('enquiry_detail/<int:pk>', views.EnquiryDetailView.as_view(), name='enquiry_detail'),
    path('enquiry_edit/<int:pk>', views.EnquiryUpdateView.as_view(), name='enquiry_edit'),
    path('send_entrance_results/<int:pk>', views.send_entrance_results, name='send_entrance_results'),
    path('send_interview_results/<int:pk>', views.send_interview_results, name='send_interview_results'),
    path('send_confirmation_email/<int:pk>', views.send_confirmation_email, name='send_confirmation_email'),
    path('send_entrance_info/<int:pk>', views.send_entrance_info, name='send_entrance_info'),
    path('enroll/<int:pk>', views.enroll, name='enroll'),
    path('ajax\show_modal', views.show_modal, name='show_modal'),

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    path('application_form/', views.application_form, name='application_form'),
    path('send_application_email/<int:pk>&<str:email>', views.send_application_email, name='send_application_email'),
    path('application_form/<int:pk>&<str:email>', views.application_form_enquiry, name='application_form'),
    path('applications/', views.ApplicationListView.as_view(), name='application_list'),
    path('application_detail/<int:pk>', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('application_edit/<int:pk>', views.ApplicationUpdateView.as_view(), name='application_edit'),
    path('ajax\app_show_modal', views.show_app_modal, name='show_application_modal'),
    path('send_app_entrance_results/<int:pk>', views.send_app_entrance_results, name='send_app_entrance_results'),
    path('send_app_interview_results/<int:pk>', views.send_app_interview_results, name='send_app_interview_results'),
    path('send_app_confirmation_email/<int:pk>', views.send_app_confirmation_email, name='send_app_confirmation_email'),
    path('send_app_entrance_info/<int:pk>', views.send_app_entrance_info, name='send_app_entrance_info'),
    path('app_enroll/<int:pk>', views.app_enroll, name='app_enroll'),
    path('enquiry_students/api/', views.enquiry_students_api, name='enquiry_students_api'),
    path('api/test/', views.enquiry_api_test, name='enquiry_students_api'),
    
]