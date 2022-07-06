 

from .models import Notification
from student_management_app.models import (Semester,CourseCategory)
from django.shortcuts import get_object_or_404
from django.urls import resolve

def notifications_data(request):
    notifications = Notification.objects.all()[:5]
    # active=request.user.email
    notification_count = Notification.objects.filter(is_seen = False).count()
    url_name = resolve(request.path).url_name
    # school_classes = Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'School'))
    # plus_two_classes = Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'Plus-Two'))
    # bachelor_classes = Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'Bachelor'))
    # master_classes = Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'Master'))


    return {
        'notification':notifications,
        'notify_count':notification_count,
        'url_name':url_name
        # 'school_classes':school_classes,
        # 'plus_two_classes':plus_two_classes,
        # 'bachelor_classes':bachelor_classes,
        # 'master_classes':master_classes
        }
  
  
  
  
  