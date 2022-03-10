
from rest_framework import routers
from django.urls import path,include
from school_apps.student.api.views import StudentApiView,UserLogViewSet

router = routers.DefaultRouter()

router.register(r'students', StudentApiView, 'students')
router.register(r'userlog', UserLogViewSet, 'userlog')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]