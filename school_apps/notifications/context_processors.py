from .models import Notification
from student_management_app.models import Semester, CourseCategory
from django.shortcuts import get_object_or_404
from django.urls import resolve
from django.urls import Resolver404

def notifications_data(request):
    # notifications = Notification.objects.all()[:5]
    # notification_count = Notification.objects.filter(is_seen=False).count()
    try:
        url_name = resolve(request.path).url_name
        
    except Resolver404:
        pass

    return {
        # "notification": notifications,
        # "notify_count": notification_count,
        "url_name": url_name,
    }
