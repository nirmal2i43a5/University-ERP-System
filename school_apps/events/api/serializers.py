
from django.db.models import fields
from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,HyperlinkedModelSerializer,HyperlinkedRelatedField
from prabhu_apps.events.models import Event

from django_filters import FilterSet

class EventSerializer(HyperlinkedModelSerializer):
    # url = HyperlinkedIdentityField(view_name="event_api:yearly_event")
    class Meta:
        model = Event
        fields = ('id','title','event_day','start_time','end_time','description','category','year',)
        

class EventFilter(FilterSet):
    class Meta:
        model = Event
        fields = '__all__'