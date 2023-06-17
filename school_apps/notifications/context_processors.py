 

from .models import Notification
from student_management_app.models import (Semester,CourseCategory)
from django.shortcuts import get_object_or_404
from django.urls import resolve

def notifications_data(request):
    notifications = Notification.objects.all()[:5]
    notification_count = Notification.objects.filter(is_seen = False).count()
    url_name = resolve(request.path).url_name
  


    return {
        'notification':notifications,
        'notify_count':notification_count,
        'url_name':url_name
       
        }
  
  
  
  
  