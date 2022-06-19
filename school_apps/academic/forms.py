from django import forms
from django.shortcuts import get_object_or_404
from school_apps.academic.models import Syllabus, Assignment, Routine,Section
from student_management_app.models import Semester, Subject,CourseCategory
from django.contrib.admin.widgets import AdminSplitDateTime




class FilterForm(forms.Form):
    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
        a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
        bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
        master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
        
        if user.adminuser.course_category == a_level_course_category:
            semester = self.fields['semester']
            semester.queryset = semester.queryset.filter(course_category = a_level_course_category)
            section = self.fields['section']
            section.queryset = section.queryset.filter(course_category = a_level_course_category)
            
        if user.adminuser.course_category == bachelor_course_category:
            semester = self.fields['semester']
            semester.queryset = semester.queryset.filter(course_category = bachelor_course_category)
            section = self.fields['section']
            section.queryset = section.queryset.filter(course_category = bachelor_course_category)
            
        if user.adminuser.course_category == master_course_category:
            semester = self.fields['semester']
            semester.queryset = semester.queryset.filter(course_category = master_course_category)
            section = self.fields['section']
            section.queryset = section.queryset.filter(course_category = master_course_category)

class SyllabusForm(forms.ModelForm):
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect(attrs={'class': 'inline'}))
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Syllabus Title",}))
    semester = forms.ModelChoiceField(label='Class',empty_label="Select Class", queryset = Semester.objects.all())
    description = forms.CharField( required = False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 10,"placeholder": " Enter  Course Description",}))

    class Meta:
        model = Syllabus
        fields = '__all__'
        




class AssignmentForm(forms.ModelForm):
    # course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
    #                                   queryset = CourseCategory.objects.all())
    
    # semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',widget=forms.Select(attrs = {'hidden':''}),
    #                                   queryset = Semester.objects.all())
    # section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',widget=forms.Select(attrs = {'hidden':''}),
    #                                  queryset = Section.objects.all())
    # subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',widget=forms.Select(attrs = {'hidden':''}),
    #                                  queryset = Subject.objects.all())
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    deadline = forms.SplitDateTimeField(label = 'Deadline', widget=AdminSplitDateTime())
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Title",}))
    description = forms.CharField( widget=forms.Textarea(attrs={'rows': 2, 'cols': 10,"placeholder": " Enter  Course Description",}))
    Subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Select Subject',
                                      queryset = Subject.objects.all()
                                     )
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ('created_by','student','assignment_category','teacher',)
        
    # def __init__(self, *args, user=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if user:
    #         subject = self.fields['Subject']
    #         subject.queryset = subject.queryset.filter(staff_user=user)
            
    #     if user.is_superuser:# or user|has_group:'Admin':#showing all subjects to superuser
    #         subject = self.fields['Subject']
    #         subject.queryset = Subject.objects.all()

class SemesterSectionSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',
                                     queryset = Section.objects.none())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',
                                     queryset = Subject.objects.none())
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))


class RoutineSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',
                                     queryset = Section.objects.none())
 
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))


class SyllabusSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
  
 
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))



class RoutineForm(forms.ModelForm):
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    # starting_time = forms.TimeField(widget=forms.TimeInput(attrs = {'type':'time',"class":"form-control"}))
    # ending_time = forms.TimeField(widget=forms.TimeInput(attrs = {'type':'time',"class":"form-control"}))
    # room = forms.CharField(required = False, widget = forms.TextInput(attrs = {'class':'form-control','placeholder':'Enter Room Name'}))
    semester = forms.ModelChoiceField(label='Class',empty_label="Select Class", queryset = Semester.objects.all())
  
    # staff = forms.ModelChoiceField(label = 'Teacher Name',
    #                                     queryset = CustomUser.objects.filter(user_type = Group.objects.get(name = 'Teacher'))
    #                                     )

    class Meta:
        model = Routine
        fields = ('course_category','routine_file','semester','section',)
    

class SubjectSearchForm(forms.Form):
    subject = forms.ModelChoiceField(label = '',empty_label="Select Subject", queryset = Subject.objects.all())
    
    def __init__(self, request, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        subject = self.fields['subject']
        subject.queryset = subject.queryset.filter(staff_user__subject = request.user.student.subject)
        
        
class SubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields = ('subject_name','subject_code','faculty')
        
        
class BachelorSubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields = ('subject_name','subject_code','bachelor_semester')
        

class MasterSubjectForm(forms.ModelForm):
    class Meta:
        model=Subject
        fields = ('subject_name','subject_code','master_semester')
        
class SemesterForm(forms.ModelForm):#for a-level
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.exclude(course_name__in = ['School']), widget=forms.RadioSelect())
    name = forms.CharField(required = False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Your Class Name'}))
    # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
    #     attrs={'placeholder': 'Enter Semester Value'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
    class Meta:
        model = Semester
        fields = ('course_category','name','description')
        
class ClassSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',
                                      empty_label = '---Click Here To  Filter Class---', 
                                      queryset = CourseCategory.objects.all())
class SectionSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',
                                      empty_label = '---Click Here To  Filter Course Category---', 
                                      queryset = CourseCategory.objects.all())
    filter_semester = forms.ModelChoiceField(label= '',
                                      empty_label = '---Click Here To  Filter Class---', 
                                      queryset = Semester.objects.all())
# class BachelorSemesterForm(forms.ModelForm):#for a-level
#     description = forms.CharField(required=False, widget=forms.Textarea(
#         attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
#     class Meta:
#         model = Semester
#         fields = ('bachelor_semester','description','name')
        
        
# class MasterSemesterForm(forms.ModelForm):#for a-level
#     description = forms.CharField(required=False, widget=forms.Textarea(
#         attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

#     class Meta:
#         model = Semester
#         fields = ('master_semester','description','name')
        
class SectionForm(forms.ModelForm):#for a-level
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.exclude(course_name__in = ['School']), widget=forms.RadioSelect())
    name = forms.CharField(required = False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Your Class Name'}))
    # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
    #     attrs={'placeholder': 'Enter Semester Value'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
    class Meta:
        model = Semester
        fields = ('course_category','name','description')
        
class SectionForm(forms.ModelForm):#for a-level
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    name = forms.CharField(required = False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Your Class Name'}))
    # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
    #     attrs={'placeholder': 'Enter Semester Value'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
    class Meta:
        model = Semester
        fields = ('course_category','name','description')
        
class SectionForm(forms.ModelForm):
 
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    # semester = forms.ModelChoiceField(queryset = Semester.objects.all(), )
    # section_name = forms.CharField(label='Section Name', widget=forms.TextInput(
    #     attrs={"class": "form-control", "placeholder": " Enter Section Name", }))
    # capacity = forms.IntegerField(required = False, label='Capacity', widget=forms.NumberInput(
    #     attrs={"class": "form-control", "placeholder": " Enter Section  Capacity", }))
  


    # def __init__(self, *args, user=None, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
    #     bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
    #     master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
        
    #     if user.adminuser.course_category == a_level_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = a_level_course_category)
    #     if user.adminuser.course_category == bachelor_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = bachelor_course_category)
    #     if user.adminuser.course_category == master_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = master_course_category)
    
    
    class Meta:
        model = Section
        fields = ['course_category','semester','section_name','capacity','description']
     

            
class ClassFormSearch(FilterForm):
 
    semester = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter Class---', queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter section---', queryset = Section.objects.all())
    

class StudentFormSearch(FilterForm):
    faculty_choices = (
                    ('', '-------Select Group-------'),
                    ('Science','Science'),
                    ('Non-Science','Non-Science')
                )
                   
    semester = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter Class---', queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter section---', queryset = Section.objects.all()) 
    group=forms.ChoiceField(required = False, label = '',choices=faculty_choices)
    
class StudentSearch(FilterForm):#For master and bachelor
    faculty_choices = (
                    ('', '-------Select Group-------'),
                    ('Science','Science'),
                    ('Non-Science','Non-Science')
                )
                   
    semester = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter Class---', queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = '---Click Here To  Filter section---', queryset = Section.objects.all()) 