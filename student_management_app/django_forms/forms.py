from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.contrib.auth.models import Group
from student_management_app.models import (
                        Course, CourseCategory, Subject, Staff, CustomUser, SessionYear, Student, Parent, Semester, Section,
                        ExtraUser, DocumentFile, StudentGroup, OptionalSubject
                        )


class DateInput(forms.DateInput):
    input_type = 'date'


class CourseForm(forms.ModelForm):
    course_name = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter  Course Name", }))
    course_code = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": " Enter  Course Code", }))
    course_description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('course_name', css_class='form-group col-md-6 mb-0'),
                Column('course_code', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
             Row(
                Column('course_description',
                       css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),

        )



class AddCustomUserForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={"placeholder": " Enter Email"}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(
        attrs={"placeholder": " Enter Full Name", }))
    # username = forms.CharField(widget=forms.TextInput(
    #     attrs={"placeholder": " Enter Username", }))#,initial='nirmal')
    # password = forms.CharField(required = False, widget=forms.PasswordInput(
    #     attrs={"placeholder": " Enter Password"}),initial='admin123')

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email',)
        # fields = ('full_name', 'email', 'username','password',)
        
    # def __init__(self, *args, **kwargs):
    #     super(AddCustomUserForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].disabled = True
    #     self.fields['username'].initial = 'admin123'
        
    '''This set password when u save or edit customuser form'''
    # def save(self, commit=True):
    #     user = super(AddCustomUserForm, self).save(commit=False)
    #     password = self.cleaned_data["password"]
    #     if password:
    #         user.set_password(password)
    #     if commit:
    #         user.save()
    #     return user


    def __init__(self, *args, **kwargs):
        super(AddCustomUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.form_id = 'student-modelform'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                   Column('full_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),
           


        )
        
        
class AddSystemAdminForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={"placeholder": " Enter Email"}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(
        attrs={"placeholder": " Enter Full Name", }))
    user_type = forms.ModelChoiceField(
        empty_label="Select Admin Group ", queryset=Group.objects.exclude(name__in = ['Student','Teacher','Parent','Procurement','Finance']))

    class Meta:
        model = CustomUser
        fields = ('user_type','full_name', 'email',)



    def __init__(self, *args, **kwargs):
        super(AddSystemAdminForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.form_id = 'student-modelform'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                 Column('user_type', css_class='form-group col-md-4 mb-0'),
                   Column('full_name', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),

                css_class='form-row'
            ),
           


        )
#I also want password field while editing so i am using separate form 
class EditCustomUserForm(forms.ModelForm):
    email = forms.EmailField(required=False, widget=forms.EmailInput(
        attrs={"placeholder": " Enter Email"}))
    full_name = forms.CharField(label='Full Name', widget=forms.TextInput(
        attrs={"placeholder": " Enter Full Name", }))
    username = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Username",'readonly':'readonly' }))#,initial='nirmal')
    # password = forms.CharField(required = False, widget=forms.PasswordInput(
    #     attrs={"placeholder": "Fill This Only If You Want To Change Password",}))

    class Meta:
        model = CustomUser
        fields = ('full_name', 'email', 'username',)
        
    # def save(self,user_id, commit=True):
    #     user = super(EditCustomUserForm, self).save(commit=False)
    #     password = self.cleaned_data["password"]
    
    #     # user_id = CustomUser.objects.get(id = user_id)
    #     # previous_password = user_id.password
        
    #     # if  password == '':
    #     #     user.set_password(previous_password)
    #     #     user.save()
        
    #     if password:#  and password!="":
    #         print("---I am password")
    #         user.set_password(password)
            
    #     if commit:
    #         user.save()
                
    #     return user
    
    def __init__(self, *args, **kwargs):
        super(EditCustomUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.form_method = 'post'
        # self.helper.form_id = 'student-modelform'
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
                # Column('password', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            )


        )



# this is for other user like driver,receptionist,accountant and others
class ExtraUserForm(forms.ModelForm):

    # role = forms.ModelChoiceField(
    #     empty_label="Select Branch ", queryset=Group.objects.exclude(name__in = ['Admin','Student','Teacher','Parent']), label="Branch")
    dob = forms.DateField(required=False, label='Date of Birth',
                          widget=forms.DateInput(attrs={'type': 'date', }))
    join_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', }))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Mobile Number", }))
    religion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": " Enter Your Religion", }))       
    address = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Address", }))

    class Meta:
        model = ExtraUser
        fields = '__all__'
        exclude = ('extra_user', 'status', 'role')

    def __init__(self, *args, **kwargs):
        super(ExtraUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # form_id and form_tag is the main to work with two form
        # self.helper.form_id = 'custom-modelform'
        # for two forms   (solve controversy for two forms)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('branch', css_class='form-group col-md-6 mb-0'),
                    Column('dob', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),
             Row(

                  Column('gender', css_class='form-group col-md-6 mb-0'),
                      Column('religion', css_class='form-group col-md-6 mb-0'),

                css_class='form-row'
            ),

               Row(
                     Column('address', css_class='form-group col-md-6 mb-0'),
                    Column('contact', css_class='form-group col-md-6 mb-0'),

                    css_class='form-row'
            ),
                Row(
                        Column('join_date', css_class='form-group col-md-6 mb-0'),
                     Column('image', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
            ),
                    Row(
               HTML(
                   '<a class="btn btn-danger" href="{% url "admin_app:manage_user" %}">Back</a>'),

            HTML('<button class="btn btn-success ml-2" name = "extrauser_submit" type="submit">Save</button>&nbsp;'),
    ),

        )


class StaffForm(forms.ModelForm):
    # courses_choices = (
    #     ('A-Level','A-Level'),('Bachelor','Bachelor'),('Master','Master')
    # )
    courses = forms.ModelMultipleChoiceField(queryset = CourseCategory.objects.all(), widget=forms.CheckboxSelectMultiple)
    dob = forms.DateField(required=False, label='Date of Birth',
                          widget=forms.DateInput(attrs={'type': 'date', }))
    join_date = forms.DateField(required = False,
        widget=forms.DateInput(attrs={'type': 'date', }))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Mobile Number", }))
    religion = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"placeholder": " Enter Your Religion", }))
    address = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Address", }))
    # full_name=forms.CharField(label = 'Full Name', widget=forms.TextInput(attrs={"placeholder": " Enter Full Name",}))
    # image=forms.ImageField(required = False, widget=forms.FileInput(attrs={
    #     'class':'form-control btn-sm bg-gray col-md-3',
    #     }))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('staff_user', 'status',)

    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        # form_id and form_tag is the main to work with two form
        # self.helper.form_id = 'custom-modelform'
        # for two forms   (solve controversy for two forms)
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('courses', css_class='form-group col-md-4 mb-0'),
                Column('dob', css_class='form-group col-md-4 mb-0'),
                   Column('gender', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
             Row(
                 Column('department', css_class='form-group col-md-6 mb-0'),
                Column('address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                Row(

                    Column('contact', css_class='form-group col-md-6 mb-0'),
                    Column('religion', css_class='form-group col-md-6 mb-0'),

                    css_class='form-row'
            ),
               Row(
                    Column('join_date', css_class='form-group col-md-6 mb-0'),
                    Column('image', css_class='form-group col-md-6 mb-0'),
                    
                    css_class='form-row'
            ),

             Row(
               HTML(
                   '<a class="btn btn-danger" href="{% url "home" %}">Back</a>'),

            HTML('<button class="btn btn-success ml-2" name = "teacher_submit" type="submit">Save</button>&nbsp;'),
    ),
        )






class DocumentFileForm(forms.ModelForm):
    # file=forms.FileField(widget=forms.FileInput(attrs={
    #     'class':'form-control btn-sm  col-md-12', 'multiple': True,
    #     }))
    title = forms.CharField(widget=forms.TextInput(
        attrs={"placeholder": " Enter Document Title", }))

    class Meta:
        model = DocumentFile
        fields = ("title", "file",)







 




class OptionalSubjectForm(forms.ModelForm):
    # I use html form for this check in add_subject.html
    semester = forms.ModelChoiceField(label = 'Class', empty_label="Select Class", queryset=Semester.objects.all())

    subject_name=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Subject Name",}))

    class Meta:
        model=OptionalSubject
        fields='__all__'
        exclude=('course',)

# session year form
class SessionYearForm(forms.ModelForm):
    session_start_year=forms.DateField(widget=DateInput)
    session_end_year=forms.DateField(widget=DateInput)
    class Meta:
        model=SessionYear
        fields='__all__'

