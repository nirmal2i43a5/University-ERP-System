from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.contrib.auth.models import Group
from student_management_app.models import (
                        Course,Subject,Staff,CustomUser,SessionYear, Student, Parent, Semester,Section,
                        ExtraUser, DocumentFile, StudentGroup
                        )

class DateInput(forms.DateInput):
    input_type = 'date'

#I am making this form just for solving name issue for guardian/full_name in parent.If i dont use this then i cannot change label of full_name with guardian namae
class ParentCustomUserForm(forms.ModelForm):
    email=forms.EmailField(required = False,widget=forms.EmailInput(attrs={"placeholder": " Enter Email"}))
    full_name=forms.CharField(label = 'Father Name', required = False, widget=forms.TextInput(attrs={"placeholder": " Enter Father Name",}))
    username=forms.CharField(widget=forms.TextInput(attrs={"placeholder": " Enter Username",}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": " Enter Password",}))
    
    class Meta:
        model = CustomUser
        fields = ('full_name','email', 'username','password',)
        
    def __init__(self, *args, **kwargs):
        super(ParentCustomUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'student-modelform'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                   Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
             
                css_class='form-row'
            ),
            Row(
                   Column('username', css_class='form-group col-md-6 mb-0'),
                #   Column('user_type', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                
                css_class='form-row'
            )
             
         
        )




#This is same as above form but does not contain button
class ParentForm(forms.ModelForm):
    # full_name=forms.CharField(label='Guardian Name',widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Guardian Name",}))
    local_guardian_name=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": " Enter Local Guardian Name",}))
    mother_name=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Mother Name",}))
    father_name=forms.CharField(required = False,widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Father Name",}))
    father_phone=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": " Enter Father Mobile Number",}))
    mother_phone=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": " Enter  Mother Mobile Number",}))
    local_guardian_phone=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": " Enter Local Guardian Mobile Number",}))
    home_phone=forms.CharField(required = False, widget=forms.TextInput(attrs={"class":"form-control", "placeholder": " Enter  Home Mobile Number",}))
    class Meta:
        model = Parent
        fields = ('home_phone','father_name',"father_phone",'local_guardian_name','local_guardian_phone','mother_name','mother_phone',)                
 
    def __init__(self, *args, **kwargs):
        super(ParentForm,self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_id = 'student_parent-modelform'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
             
                Column('home_phone', css_class='form-group col-md-6 mb-0'),
               Column('father_name', css_class='form-group col-md-6 mb-0'),
                
                css_class='form-row'
            ),
             Row(
                  Column('father_phone', css_class='form-group col-md-6 mb-0'),
                    Column('mother_name', css_class='form-group col-md-6 mb-0'),
                  
                css_class='form-row'
            ),
                Row(
                   
                    Column('mother_phone', css_class='form-group col-md-6 mb-0'),
                    Column('local_guardian_name', css_class='form-group col-md-6 mb-0'),
                                 
                    css_class='form-row'
            ),
                            Row(
                   
                    Column('local_guardian_phone', css_class='form-group col-md-6 mb-0'),
                    
                                #  Column('image', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
            ),
                          
             
                Row(
            HTML('<a class="btn btn-danger" href="{% url "dashboard" %}">Back</a>'),
                         
            HTML('<button class="btn btn-success ml-2" type="submit" name = "parent_submit">Save</button>&nbsp;'),
    ) ,
            
        )
