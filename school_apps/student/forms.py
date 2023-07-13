from django import forms
from student_management_app.models import Student,Section,Semester,CourseCategory,Course
from django.shortcuts import get_object_or_404
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
gender_choices = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others')
)
class StudentForm(forms.ModelForm):
    # guardian = forms.ModelChoiceField(required=True, label='Parent Name',
    #                                   empty_label="-----Please Select Your Parent Name----- ", queryset=Parent.objects.all())
    status_choices = (
        ('Running','Running'),('In Active','In Active')
    )
    shift = (
        ('Morning','Morning'),
          ('Day','Day')
    )
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    course = forms.ModelChoiceField(required = False, queryset = Course.objects.all())
    section = forms.ModelChoiceField(
        required = False,empty_label="Select Section ", queryset=Section.objects.all())
    dob = forms.DateField(label='Date of Birth', widget=forms.DateInput(
        attrs={'type': 'date', "class": "form-control"}))
    status = forms.ChoiceField(choices=status_choices, widget=forms.RadioSelect(),initial = 'Running')
    shift = forms.ChoiceField(choices=shift, widget=forms.RadioSelect(),initial = 'Morning')
    gender = forms.ChoiceField(choices=gender_choices, widget=forms.RadioSelect(),initial = 'Male')
    stu_id = forms.CharField(label='Roll No.',required = False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter Roll No", }))
    roll_no = forms.CharField(label='Student Id.',required=True, widget=forms.TextInput(
        attrs={"placeholder": " Enter Matrix Number", }))
    temporary_address = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter Temporary Address", }))
    
    permanent_address = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter permanent Address", }))
    gpa = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter Your Previous GPA", }))
    previous_school_name = forms.CharField(required=False,label = 'Past School/College', widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter Your Past School Name", }))
    contact = forms.CharField(required=False, widget=forms.TextInput(
        attrs={"class": "form-control", "placeholder": " Enter Student Mobile Number", }))
   

    semester = forms.ModelChoiceField(
        label='Class', empty_label="Select Class ", queryset=Semester.objects.all())
# ----------
 
    class Meta:
        model = Student
        fields = (
           'course_category', 'course','semester','section','join_year','stu_id','roll_no','gender',
           'shift',
           'faculty','program',
           'status','contact',
            'permanent_address','temporary_address','dob','blood_group','gpa','previous_school_name','image',
        )

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()        
        self.helper.form_tag = False
        self.helper.form_method = 'post'
        self.helper.form_id = 'student-formhelper'
        self.helper.layout = Layout(
             Row(
                Column('course_category', css_class='form-group col-md-6 mb-0'),
                Column('course', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
                 Row(
                Column('semester', css_class='form-group col-md-4 mb-0'),
                     
                        Column('section', css_class='form-group col-md-4 mb-0'),
                        Column('join_year', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                        
                
                Column('roll_no', css_class='form-group col-md-4 mb-0'),
                 Column('stu_id', css_class='form-group col-md-4 mb-0'),
                Column('gender', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
             Row(
                  Column('shift', css_class='form-group col-md-4 mb-0'),
               
                     Column('status', css_class='form-group col-md-4 mb-0'),
                    Column('contact', css_class='form-group col-md-4 mb-0'),
                
                css_class='form-row'
            ),
            Row(
                         Column('permanent_address', css_class='form-group col-md-4 mb-0'),
                
                       Column('temporary_address', css_class='form-group col-md-4 mb-0'),
               
                              Column('dob', css_class='form-group col-md-4 mb-0'),
                              

                
                css_class='form-row'
            ),
           
               Row(
                    Column('blood_group', css_class='form-group col-md-4 mb-0'),
                  
                      Column('gpa', css_class='form-group col-md-4 mb-0'),
                           Column('previous_school_name', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
            ),
                  Row(
                  
                                                      Column('image', css_class='form-group col-md-4 mb-0'),

                    css_class='form-row'
            ),
               
                
        )