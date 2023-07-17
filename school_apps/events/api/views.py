from nepalicalendar.nepdate import NepDate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from school_apps.events.models import Event
from .serializers import EventSerializer, EventFilter
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.filters import SearchFilter


class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    # permission_required = 'events.view_event'
    http_method_names = ["get"]


class UpcomingEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(category="Event")
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]
    # filter_backends = [SearchFilter]
    # search_fields = ['title','event_day','english_date','year']

    def get_queryset(self, *args, **kwargs):
        queryset_list = Event.objects.filter(category="Event")
        query = self.request.GET.get("search")

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                | Q(event_day__icontains=query)
                | Q(year__icontains=query)
            ).distinct()
        return queryset_list


class UpcomingHolidayViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(category="Holiday")
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ["get"]

    def get_queryset(self, *args, **kwargs):
        queryset_list = Event.objects.filter(category="Holiday")
        query = self.request.GET.get("search")

        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query)
                | Q(event_day__icontains=query)
                | Q(year__icontains=query)
            ).distinct()
        return queryset_list
