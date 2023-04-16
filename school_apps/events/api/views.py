
from nepalicalendar.nepdate import NepDate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from prabhu_apps.events.models import Event
from .serializers import (EventSerializer,EventFilter)
from rest_framework import permissions, status,viewsets
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.filters import SearchFilter


    
class EventApiView(viewsets.ViewSet):
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    serializer_class = EventSerializer
    # filter_backends = [SearchFilter]
    # search_fields = ['title']

    def list(self, request):
        events_qs = Event.objects.filter(category = 'Event')
        holidays_qs = Event.objects.filter(category = 'Holiday')
        today_event_qs = Event.objects.filter(event_day = NepDate.today())
        
            
        event_serializers = EventSerializer(events_qs, many=True)
        holidays_serializers = EventSerializer(holidays_qs, many=True, context={'request': request})
        today_event_serializers = EventSerializer(today_event_qs, many=True)
        
        serializer_list = {
                            'today_events': today_event_serializers.data,
                           'upcoming_holidays':holidays_serializers.data,
                           'upcoming_events':event_serializers.data
                           }
                       
        # serializer_list = [event_serializers.data, holidays_serializers.data, today_event_serializers.data]
        return Response(serializer_list, status=status.HTTP_200_OK)
    

    
    def create(self, request):
        event_serializers = EventSerializer(data=request.data) 
        event_serializers.is_valid(raise_exception=True)
        event_serializers.save()
        return Response(event_serializers.data, status=status.HTTP_201_CREATED)
    
    
    def retrieve(self, request, pk=None):
        event = get_object_or_404(Event, pk = pk)
        event_serializers = EventSerializer(event, many = False)
        return Response(event_serializers.data, status=status.HTTP_200_OK)


    def update(self, request, pk=None, ):
        event = get_object_or_404(Event, pk = pk)
        event_serializers = EventSerializer(instance=event, data=request.data)
        event_serializers.is_valid(raise_exception=True)
        event_serializers.save()
        return Response(event_serializers.data, status=status.HTTP_200_OK)

    def delete(self,request, pk=None, ):
        event = get_object_or_404(Event, pk = pk)
        event.delete()
        return Response({'message': 'Event is deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class UpcomingEventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(category = 'Event')
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    # filter_backends = [SearchFilter]
    # search_fields = ['title','event_day','english_date','year']
        
    def get_queryset(self, *args, **kwargs):
        queryset_list = Event.objects.filter(category = 'Event') 
        query = self.request.GET.get("search")
        
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(event_day__icontains=query)|
                    Q(year__icontains=query)
                    
                    ).distinct()
        return queryset_list
    

   
class UpcomingHolidayViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.filter(category = 'Holiday')
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get']
    def get_queryset(self, *args, **kwargs):
        queryset_list = Event.objects.filter(category = 'Holiday')
        query = self.request.GET.get("search")
        
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(event_day__icontains=query)|
                    Q(year__icontains=query)
                    
                    ).distinct()
        return queryset_list


@api_view(['GET'])
def yearly_event_view(request, *args, **kwargs):
    slug = request.GET.get('year')
    yearly_events = Event.objects.filter(year = slug).values()
    serializer = EventSerializer(yearly_events, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def today_events(request, *args, **kwargs):
    todays_events = Event.objects.filter(event_day = NepDate.today())
    print(today_events)
    serializer = EventSerializer(todays_events, many=True)
    return Response(serializer.data, status=200)
   