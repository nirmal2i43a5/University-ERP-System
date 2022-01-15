from django.urls import path
from school_apps.customusers.views import *
app_name = 'customuser'
urlpatterns = [
    path('manage_customuser/',manage_customuser,name = 'manage_customuser',),
       path('cutomuser/edit/<pk>/',edit_customuser,name = 'edit_customuser',)
]
