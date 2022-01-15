from django import template
from django.shortcuts import redirect
from django.http.response import HttpResponse
from django.shortcuts import render

from django.contrib import messages
from school_apps import notifications
from .models import Notification
from django.contrib.auth.decorators import login_required, permission_required


def show_notification(request):
	notifications = Notification.objects.all().order_by('-id')
	context = {
		'notifications': notifications,
		'title':'Notifications'
	}
	return render(request,'notifications/notifications.html',context)


def update_notification(request):#ajax call when click on notification icon and make notification zero after is_seen = True
    notifications = Notification.objects.filter(is_seen=False)
    for post in notifications:
        post.is_seen = True
        post.save()
    return HttpResponse("OKAY")



@permission_required('notifications.delete_notifications', raise_exception=True)
def delete_notification(request):
    Notification.objects.all().delete()
    messages.success(request,"Successfully deleted all notifications.")
    return redirect('notifications:show-notifications')
    


def notification_detail(request,pk):
    notification_detail = Notification.objects.filter(pk=pk).first()
    context = {
        'title':'Notification Detail',
        'notification_detail':notification_detail
    }
    return render(request,'notifications/notification_detail.html',context)
    
    