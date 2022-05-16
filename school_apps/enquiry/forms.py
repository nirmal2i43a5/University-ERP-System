from django import forms
from django.forms import fields
from .models import Enquiry, Application

class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = '__all__'
        exclude = ('called','status','remarks','entrance_marks', 'entrance_result', 'interview_result',
                    'application_sent', 'entrance_result_sent', 'interview_result_sent')

class EnquiryUpdateForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    address = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    home_contact = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    mobile_no = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # enquiry = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=Enquiry
        fields='__all__'


class ApplicationForm(forms.ModelForm):
    dob = forms.DateField(required=False, label='Date of Birth',
                          widget=forms.DateInput(attrs={'type': 'date', }))
    class Meta:
        model=Application
        fields='__all__'
        exclude = ('status','entrance_marks', 'entrance_result', 'interview_result',
                     'entrance_result_sent', 'interview_result_sent')


class ApplicationUpdateForm(forms.ModelForm):
    name = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    temporary_address = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    home_phone = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    contact_no = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    email = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    # enquiry = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=Application
        fields=['name', 'temporary_address', 'email', 'home_phone', 'contact_no', 'status', 
                 'entrance_marks', 'entrance_result', 'entrance_result_sent', 'interview_result', 'interview_result_sent']
        