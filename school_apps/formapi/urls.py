
from django.urls import path
from .views import *

app_name = 'formapi'



urlpatterns= [
    path('template_editor/', formbuilder, name='form_builder'),             #edit form
    path('create-form-template/', formbuilder_select, name='form_builder_select'),      
    path('edit-forms-select/',formTemplateListView.as_view(), name='form_edit_select'),
    path('edit-form/<int:pk>',edit_form,name='edit_form'),
    path('forms/submit', formsubmit, name='form_submit'),
    path('admission-form-select/', admissionform_select, name='admissionform_select'),   
    path('submit/', form_submit_view, name='admissionform_submit'),  
    path('select/', form_selection, name='form_select'), 
    # path('application_form',),

    path('viewtemplates/', viewtemplates, name='viewtemplates'),
    path('forms/<pk>/', api_detail_view, name='details'),
    path('forms/<pk>/update', api_update_view, name='update'),
    path('forms/create', api_create_view, name='create'),
    path('forms/<pk>/dataset', prepopulate, name='api_dataset'),
    path('forms/dataset/<str:pk>', prepopulate_courses, name='api_dataset_dept'),

    path('forms/', allforms, name='allforms'),
    
]
