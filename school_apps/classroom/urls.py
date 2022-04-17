from django.urls import path
from .views import class_home


app_name = 'classroom'

urlpatterns = [
      
    path('classroom/', class_home, name="class-home"),
    
]
