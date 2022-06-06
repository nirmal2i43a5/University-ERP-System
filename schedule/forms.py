from django import forms
from django.utils.translation import gettext_lazy as _

from schedule.models import Event,Occurrence
from schedule.models import Calendar
# from calendar_app.models  import Event
from schedule.widgets import ColorInput

from django.contrib.admin.widgets import   AdminSplitDateTime

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
# from django.forms.widgets import Input
from ckeditor.widgets import CKEditorWidget


class SpanForm(forms.ModelForm):
    start = forms.SplitDateTimeField(label = 'Start Time', widget=AdminSplitDateTime())
   	# 'start':forms.DateInput(attrs={'type':'datetime-local'},format='%Y-%m-%d'),
    # start = forms.CharField(widget = forms.DateInput(attrs={'type':'datetime-local'})),
    end = forms.SplitDateTimeField(label = 'End Time',widget=AdminSplitDateTime())
    def clean(self):
        if "end" in self.cleaned_data and "start" in self.cleaned_data:
            if self.cleaned_data["end"] <= self.cleaned_data["start"]:
                raise forms.ValidationError(
                    _("The end time must be later than start time.")
                )
        return self.cleaned_data
    
    
class EventForm(SpanForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    color_event = forms.CharField(required = False, widget = forms.TextInput(attrs = {'type':'color',}))
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Enter Event Title',}))
    description = forms.CharField(required=False,widget=CKEditorWidget())
   
    class Meta:
        model = Event
        exclude = ("creator", "created_on", "calendar",'rule','end_recurring_period',)
        widgets = {"color_event": ColorInput,
                # 'start':forms.DateTimeInput(attrs={'type':'datetime-local'},format='%m/%d/%Y %H:%M:%S'),
                # 'end':forms.DateTimeInput(attrs={'type':'datetime-local'},format='%m/%d/%Y %H:%M:%S'),
                   }
     
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                    Column('title', css_class='form-group col-md-6  mb-0'),
                         Column('color_event', css_class='form-group col-md-6 mb-0'),
                         
                  
                css_class='form-row'
            ),
        
            Row(
                 
                    Column('start', css_class='form-group col-md-6 mt-4 mb-0'),
                    Column('end', css_class='form-group col-md-6 mt-4 mb-0'),
            ),
            Row(
                 
                  Column('description', css_class='form-group col-md-6 mt-4  mb-0'),
            ),
            Row(
               HTML(
                   '<a class="btn btn-danger text-white" href="{% url "manage_event" %}">Back</a>'),

            HTML('<button class="btn btn-success ml-2" type="submit">Save</button>&nbsp;'),
    ),
             
           
        )
        





class OccurrenceForm(SpanForm):
    class Meta:
        model = Occurrence
        exclude = ("original_start", "original_end", "event", "cancelled")


class EventAdminForm(forms.ModelForm):
    class Meta:
        exclude = []
        model = Event
        widgets = {"color_event": ColorInput}



class CalendarForm(forms.ModelForm):
    class Meta:
        model = Calendar
        fields = ('name',)