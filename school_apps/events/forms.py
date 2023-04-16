from django import forms
from django.contrib.auth.models import Group
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Event


class EventForm(forms.ModelForm):
    # group = forms.ModelChoiceField(required = False, empty_label = '-------Select this for sending -----',queryset=Group.objects.all())
    class Meta:
        fields = '__all__'
        model = Event
        # exclude = ('description',)
        widgets={
        'title':forms.TextInput(attrs={'placeholder':'Enter Event Title'}),
		'start_time':forms.TimeInput(attrs={'type':'time'}),
        'end_time':forms.TimeInput(attrs={'type':'time'}),
        
         'event_day':forms.TextInput(attrs={'class':'date-picker','data-single':'true','placeholder':'Select Event Date'}),
		}
        
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()        
        self.helper.form_tag = False#for two forms   (solve controversy for two forms)
       
        self.helper.layout = Layout(
            Row(
                 Column('title', css_class='form-group col-md-4 mb-0'),
                
                Column('event_day', css_class='form-group col-md-4 mb-0'),
                      Column('category', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
             Row(
                   Column('start_time', css_class='form-group col-md-6 mb-0'),
               
                  Column('end_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                Row(
                         Column('group', css_class='form-group col-md-6 mb-0'),
                       Column('description', css_class='form-group col-md-6 mb-0'),
               
                  
                    css_class='form-row'
            ),
                     Row(
            HTML('<a class="btn btn-danger" href="{% url "calendar:home" %}">Back</a>'),
                         
            HTML('<button class="btn btn-success ml-1" type="submit">Save</button>'),
   
    ) ,
        )

  


    




    
