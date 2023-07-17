from django.shortcuts import render, redirect
from django.contrib import messages
from school_apps.announcement.forms import HolidayForm, NoticeForm
from school_apps.announcement.models import Holiday, Notice
from schedule.models import Event


def notice_log(request):
    notices_logs = Notice.history.all()
    context = {
        "title": "Notice Log",
        "notices_logs": notices_logs,
    }
    return render(
        request,
        "announcements/loghistory/individuals/notice.html",
        context)


def delete_notice_log(request):
    Notice.history.all().delete()
    messages.success(request, "Notice logs are deleted successfully.")
    return redirect("announcement:notice_log")


def event_log(request):
    events_logs = Event.history.all()

    context = {
        "title": "Event Log",
        "events_logs": events_logs,
    }
    return render(
        request,
        "announcements/loghistory/individuals/event.html",
        context)


def delete_event_log(request):
    Event.history.all().delete()
    messages.success(request, "Event logs are deleted successfully.")
    return redirect("announcement:event_log")


def all_announcement_log(request):
    events_logs = Event.history.all()
    notices_logs = Notice.history.all()
    context = {
        "title": "Event Log",
        "events_logs": events_logs,
        "notices_logs": notices_logs,
    }
    return render(request, "announcements/loghistory/allhistory.html", context)


def delete_all_log(request):
    Event.history.all().delete()
    Notice.history.all().delete()
    messages.success(request, "Announcement logs are deleted successfully.")
    return redirect("announcement:event_log")
