from django.urls import path
from . import views
from school_apps.student.student_views.views import *

app_name = 'parent'

urlpatterns=[
    path('student/', student_view_by_parent, name='student_view_by_parent'),



]