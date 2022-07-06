from django.urls import path
from school_apps.classroom.views import (
                                            classroom,plus_two_class,bachelor_class,master_class,school_classroom_contents
                                            )


app_name = 'classroom'

urlpatterns = [
      
    path('school/classroom/',classroom,name = "school-classroom"),
    path('plus-two/classroom/',classroom,name = "plus-two-classroom"),
    path('bachelor/classroom/',classroom,name = "bachelor-classroom"),
    path('master/classroom/',classroom,name = "master-classroom"),
    path('classroom/<str:pk>/',school_classroom_contents,name = "classroom-contents"),
    
]
