from rest_framework import serializers
from .models import Event


class EventsSerializer(serializers.ModelSerializer):
    time_range = serializers.SerializerMethodField()

    def get_time_range(self, obj):
        return '{} To {}'.format(obj.start_time, obj.end_time) 
    class Meta:
        model = Event
        fields = "__all__"