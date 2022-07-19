
from rest_framework import routers
from django.urls import path,include
from school_apps.student.api.views import StudentApiView
from school_apps.log_history.views import LogViewSet,AcademicLogViewSet,ParticularUserLogViewSet

router = routers.DefaultRouter()

router.register(r'students', StudentApiView, 'students')
router.register(r'userlog', LogViewSet, 'userlog')
router.register(r'academiclog', AcademicLogViewSet, 'userlog')
router.register(r'particularuserlog', ParticularUserLogViewSet, 'particularuserlog')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]