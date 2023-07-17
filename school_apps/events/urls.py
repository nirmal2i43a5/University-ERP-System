from django.conf.urls import url
from django.urls import path
from . import views
from student_management_system.views import event_home

app_name = "calendar"

urlpatterns = [
    path("event-management/", views.MonthlyCalendar.as_view(), name="home"),
    path("events/", views.EventListView.as_view(), name="event_index"),
    path("upcomingevents/", views.event_list_only, name="event_list_only"),
    path(
        "upcomingholidays/",
        views.holiday_list_only,
        name="holiday_list_only"),
    path("event/today/", views.today_event, name="today_event"),
    path("event/add/", views.EventCreateView.as_view(), name="event_create"),
    path("event/edit/<pk>/", views.EventEditView.as_view(), name="event_edit"),
    path(
        "event/delete/<pk>/",
        views.EventDeleteView.as_view(),
        name="event_delete"),
    url(r"^(?P<year>[0-9]{4})$",
        views.MonthlyCalendar.as_view(),
        kwargs={"month": 1}),
    url(
        r"^(?P<year>\d+)/(?P<month>[0-9][0-2]?)$",
        views.MonthlyCalendar.as_view(),
        name="calendar",
    ),
    # path('event-detail/',views.event_detail_view, name = 'event_detail'),
    path("event-detail/<str:date>/", views.event_detail, name="event_detail"),
    path(
        "holiday-detail/<str:date>/",
        views.holiday_detail,
        name="holiday_detail"),
    #  path('event-management/',event_home,name = 'event-management'),
]
