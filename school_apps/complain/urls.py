from django.urls import path
from school_apps.complain.views import *
from student_management_system.views import complain_home


app_name = 'complain'

urlpatterns = [
            #for complain
      
      path('add_complain/', add_complain, name="add_complain"),
      path('manage_complain/', manage_complain, name="manage_complain"),
      path('edit_complain/<str:complain_id>/', edit_complain, name="edit_complain"),
      path('delete_complain/<str:complain_id>/', delete_complain, name="delete_complain"),
      
      path('complain-management/', complain_home,name = 'complain-management'),#for dynamic sidebar
]
