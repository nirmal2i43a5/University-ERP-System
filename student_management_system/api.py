
from rest_framework import routers
from django.urls import path,include
from school_apps.student.api.views import StudentApiView
from school_apps.log_history.views import LogViewSet,AcademicLogViewSet,ParticularUserLogViewSet,AnnouncementLogViewSet,AttendanceLogViewSet
from school_apps.events.api.views import EventsViewSet,UpcomingEventViewSet,UpcomingHolidayViewSet
router = routers.DefaultRouter()

router.register(r'events', EventsViewSet, 'events')
router.register(r'upcomingevents', UpcomingEventViewSet, 'upcomingevents')
router.register(r'upcomingholidays', UpcomingHolidayViewSet, 'upcomingholidays')
router.register(r'students', StudentApiView, 'students')
router.register(r'userlog', LogViewSet, 'userlog')
router.register(r'academiclog', AcademicLogViewSet, 'userlog')
router.register(r'particularuserlog', ParticularUserLogViewSet, 'particularuserlog')
router.register(r'announcementlog', AnnouncementLogViewSet, 'annoncementlog')
router.register(r'attendancelog', AttendanceLogViewSet, 'attendancelog')

app_name = 'api'


urlpatterns = [
    
      path('', include(router.urls))
]