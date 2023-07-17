from django.db.models import fields
from rest_framework import serializers
from .models import formTemplate
from school_apps.enquiry.models import Application


class formTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = formTemplate
        fields = "__all__"


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
