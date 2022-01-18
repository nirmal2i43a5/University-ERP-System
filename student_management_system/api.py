
from rest_framework import routers
from django.urls import path,include
from school_apps.student.api.views import StudentApiView

router = routers.DefaultRouter()

router.register(r'students', StudentApiView, 'students')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]