from django.shortcuts import render
from .models import UserLog
from .serializers import UserLogSerializer
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from school_apps.log_history.models import UserLog


# @permission_required("authentication.view_user_log", raise_exception=True)
def user_log_list(request):
    context = {
        "title": "User Log",
        "active_menu": "authentication",
    }
    return render(request, "userlog/userlog.html", context=context)


def academic_log(request):
    context = {
        "title": "Academic Log",
    }
    return render(request, "userlog/academiclog.html", context)


def attendance_log(request):
    context = {
        "title": "Attendance Log",
    }
    return render(request, "userlog/attendancelog.html", context)


def announcement_log(request):
    context = {
        "title": "Announcement Log",
    }
    return render(request, "userlog/announcementlog.html", context)


class LogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.order_by("-id")
    serializer_class = UserLogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def filter_queryset(self, queryset):
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                user_id=self.request.GET.get("id")).order_by("-id")
        return queryset


class AcademicLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.filter(app_name="academic").order_by("-id")
    serializer_class = UserLogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def filter_queryset(self, queryset):
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                user_id=self.request.GET.get("id")).order_by("-id")
        return queryset


class AnnouncementLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.filter(app_name="announcement").order_by("-id")
    serializer_class = UserLogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def filter_queryset(self, queryset):
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                user_id=self.request.GET.get("id")).order_by("-id")
        return queryset


class AttendanceLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.filter(app_name="attendance").order_by("-id")
    serializer_class = UserLogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def filter_queryset(self, queryset):
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                user_id=self.request.GET.get("id")).order_by("-id")
        return queryset


class ParticularUserLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.filter(
        model_name__in=["student", "staff", "parent", "extrauser"]
    ).order_by("-id")

    serializer_class = UserLogSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def filter_queryset(self, queryset):
        if self.request.GET.get("id"):
            queryset = queryset.filter(
                user_id=self.request.GET.get("id")).order_by("-id")
        return queryset
