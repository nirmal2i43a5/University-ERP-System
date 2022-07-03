from django.urls import path
from school_apps.classroom.views import (
                                            school_class,plus_two_class,bachelor_class,master_class,classroom_contents
                                            )


app_name = 'classroom'

urlpatterns = [
      
    path('school/classroom/',school_class,name = "school-classroom"),
    path('plus-two/classroom/',plus_two_class,name = "plus-two-classroom"),
    path('bachelor/classroom/',bachelor_class,name = "bachelor-classroom"),
    path('master/classroom/',master_class,name = "master-classroom"),
    path('classroom/<str:pk>/',classroom_contents,name = "classroom-contents"),
    
]
