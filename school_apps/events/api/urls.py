from django.urls import path, include
from prabhu_apps.events.api.views import *
from rest_framework.routers import DefaultRouter

app_name = 'event_api'

# router = DefaultRouter()
# router.register('', EventApiView, basename='event')
# urlpatterns = router.urls


urlpatterns = [
    path('', EventApiView.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    ), name='event_list_or_create'),
    path('edit/<pk>/', EventApiView.as_view(
        {
            'put': 'update',
            'get': 'retrieve'
        }
    ), name='event_detail_get_or_update'),

    # dont pass slug for ?slug = slug end point as it is get
    path('year/', yearly_event_view, name='yearly_event'),
    # http://127.0.0.1:8000/api/v1/event/year/?slug=2081
    path('today/', today_events, name='today_events'),


]
