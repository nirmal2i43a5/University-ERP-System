 

from .models import Notification

def notifications_data(request):
    notifications = Notification.objects.all()[:5]
    # active=request.user.email
    notification_count = Notification.objects.filter(is_seen = False).count()
    return {'notification':notifications,'notify_count':notification_count}
  
  
  
  
  