from django import  forms
import datetime
import calendar
from django.forms.widgets import HiddenInput
from django.shortcuts import get_object_or_404
from student_management_app.models import Semester, Section, Subject,CourseCategory,Course
from .models import AttendanceReport


faculty_choices = (
        ('', '-------Select Group-------'),
        ('Science','Science'),
        ('Non-Science','Non-Science')
    )
#for taking attendance
class AttendanceFormSearch(forms.Form):

    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    filter_course = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Course',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Course.objects.all())
    filter_semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',widget=forms.Select(attrs = {'hidden':''}),
                                      queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Section.objects.all())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Subject.objects.all())
  
    
   
    # subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Select Subject',widget=forms.Select(attrs={'class':''}),
    #                                   queryset = Subject.objects.all()
    #                                  )
    # https://medium.com/analytics-vidhya/django-how-to-pass-the-user-object-into-form-classes-ee322f02948c
    # def __init__(self, *args, user=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         subject = self.fields['subject']
    #         subject.queryset = subject.queryset.filter(staff_user=user)
    #     if user.is_superuser:# or user|has_group:'Admin':
    #         subject = self.fields['subject']
    #         subject.queryset = Subject.objects.all()
            
            
    # def __init__(self, *args, user = None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    #     bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    #     master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
        
    #     if user.adminuser.course_category == a_level_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = a_level_course_category)
    #         section = self.fields['section']
    #         section.queryset = section.queryset.filter(course_category = a_level_course_category)
    #         subject = self.fields['subject']
    #         subject.queryset = subject.queryset.filter(course_category = a_level_course_category)
            
    #     if user.adminuser.course_category == bachelor_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = bachelor_course_category)
    #         section = self.fields['section']
    #         section.queryset = section.queryset.filter(course_category = bachelor_course_category)
    #         subject = self.fields['subject']
    #         subject.queryset = subject.queryset.filter(course_category = bachelor_course_category)
            
    #     if user.adminuser.course_category == master_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = master_course_category)
    #         section = self.fields['section']
    #         section.queryset = section.queryset.filter(course_category = master_course_category)
    #         subject = self.fields['subject']
    #         subject.queryset = subject.queryset.filter(course_category = master_course_category)
 
 
class AttendanceForm(forms.Form):
    attendance_date = forms.DateField(label = '', widget=forms.DateInput(attrs = {'type':'date','class':''}),initial=datetime.date.today)
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    course = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Course',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Course.objects.all())
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',widget=forms.Select(attrs = {'hidden':''}),
                                      queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Section.objects.all())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Subject.objects.all())
 
    # def __init__(self, *args, user=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         subject = self.fields['subject']
    #         subject.queryset = subject.queryset.filter(staff_user=user)
    #     if user.is_superuser:# or user|has_group:'Admin':
    #         subject = self.fields['subject']
    #         subject.queryset = Subject.objects.all()
            
            
#for managing details
class StudentAttendanceDetailsSearch(forms.Form):
    attendance_date = forms.DateField(label = '', widget=forms.DateInput(attrs = {'type':'date','class':'col-md-12'}),initial=datetime.date.today)

    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.all(),widget=forms.Select(attrs = {'class':'col-md-12'}))
    group=forms.ChoiceField(required = False, label = '',choices=faculty_choices)
    



class StudentAttendanceEditDetailsSearch(forms.Form):
    edit_filter_attendance_date = forms.DateField(label = '', widget=forms.DateInput(attrs = {'type':'date','class':'col-md-12'}),initial=datetime.date.today)
    edit_flter_semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.all())
    edit_filter_group=forms.ChoiceField(required = False, label = '',choices=faculty_choices)
    
    
    
#for respective student
class StudentAttendanceDateFilterForm(forms.Form):#for respective user not for taking attendance
    # subject = forms.ModelChoiceField(empty_label = 'Select Subject',widget=forms.Select(attrs={}),
    #                                  queryset = Subject.objects.all())
    start_date = forms.DateField( widget=forms.DateInput(attrs = {'type':'date','class':''}))
    end_date = forms.DateField(widget=forms.DateInput(attrs = {'type':'date','class':''}))


#for teacher and normal user
class AttendanceDateFilterForm(forms.Form):#for respective user not for taking attendance
    start_date = forms.DateField( widget=forms.DateInput(attrs = {'type':'date','class':''}))
    end_date = forms.DateField(widget=forms.DateInput(attrs = {'type':'date','class':''}))

#for teachers and users
class AttendanceDetailsSearch(forms.Form):
    attendance_date = forms.DateField(label = '', widget=forms.DateInput(attrs = {'type':'date','class':''}),initial=datetime.date.today)
    
    
class FilterMonthlyAttendance(forms.Form):
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    today_month = datetime.date.today().month
    month =forms.ChoiceField(required = False, label = '',choices=MONTH_CHOICES, initial=today_month)
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',widget=forms.Select(attrs = {'hidden':''}),
                                      queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Section.objects.all())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',widget=forms.Select(attrs = {'hidden':''}),
                                     queryset = Subject.objects.all())
    group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
                          widget=forms.Select(attrs = {'hidden':''}))
    
class AttendanceStatusForm(forms.ModelForm):
    class Meta:
        model = AttendanceReport
        fields = ['status']
        
        
