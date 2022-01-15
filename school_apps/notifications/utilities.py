from .models import Notification

def create_notification(request,post, notification_type,created_by,type):
    notification = Notification.objects.create(post=post,notification_type=notification_type, created_by=created_by,  type=type)
    
# def update_notification(request,post, notification_type,created_by,type):
#     notification = Notification.objects.create(post=post,notification_type=notification_type, created_by=created_by,  type=type)