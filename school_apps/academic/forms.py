from django import forms
from django.shortcuts import get_object_or_404
from school_apps.academic.models import Syllabus, Assignment, Routine,Section,Enotes
from student_management_app.models import Semester, Subject,CourseCategory,Course,Staff, SubjectTeacher,SemesterTeacher
from django.contrib.admin.widgets import AdminSplitDateTime

from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

# 500kb = 524288
# 1MB - 1048576
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "1048576"




class FilterForm(forms.Form):
    def __init__(self, *args, user = None, **kwargs):
        super().__init__(*args, **kwargs)
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
            
    #     if user.adminuser.course_category == bachelor_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = bachelor_course_category)
    #         section = self.fields['section']
    #         section.queryset = section.queryset.filter(course_category = bachelor_course_category)
            
    #     if user.adminuser.course_category == master_course_category:
    #         semester = self.fields['semester']
    #         semester.queryset = semester.queryset.filter(course_category = master_course_category)
    #         section = self.fields['section']
    #         section.queryset = section.queryset.filter(course_category = master_course_category)

class SyllabusForm(forms.ModelForm):
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect(attrs={'class': 'inline'}))
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Syllabus Title",}))
    semester = forms.ModelChoiceField(label='Class',empty_label="Select Class", queryset = Semester.objects.all())
    description = forms.CharField( required = False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 10,"placeholder": " Enter  Course Description",}))

    class Meta:
        model = Syllabus
        fields = '__all__'
        

class ENoteForm(forms.ModelForm):
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect(attrs={'class': 'inline'}))
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Syllabus Title",}))
    description = forms.CharField( required = False, widget=forms.Textarea(attrs={'rows': 2, 'cols': 10,"placeholder": " Enter  Course Description",}))

    class Meta:
        model = Enotes
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
    # course_category.course = forms.ModelChoiceField(queryset = Course.objects.all(), widget=forms.RadioSelect())
    deadline = forms.SplitDateTimeField(label = 'Deadline', widget=AdminSplitDateTime())
    title=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","placeholder": " Enter Title",}))
    description = forms.CharField( widget=forms.Textarea(attrs={'rows': 2, 'cols': 10,"placeholder": " Enter  Course Description",}))
    Subject = forms.ModelChoiceField(empty_label = 'Select Subject',
                                      queryset = Subject.objects.all()
                                     )

    def clean(self):
        self.check_file()
        return self.cleaned_data

    def check_file(self):
        content = self.cleaned_data["file"]
        content_type = content.content_type.split('/')[0]
        if content.size > int(MAX_UPLOAD_SIZE):
            raise forms.ValidationError(_("Please keep file size under %s. Current file size %s")%(filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content.size)))
        return content
    
    class Meta:
        model = Assignment
        fields = '__all__'
        exclude = ('created_by','student','teacher',)
        
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user.groups.filter(name='Teacher'):
            course_category = self.fields['course_category']
            course_category.queryset = user.staff.courses.all()
        if user.is_superuser or  user.groups.filter(name='Super-Admin') or user.groups.filter(name='Admin'):
            course_category = self.fields['course_category']
            course_category.queryset = CourseCategory.objects.all()

class SemesterSectionSearchForm(forms.Form):
    # course_category = forms.ModelChoiceField(empty_label = 'Choose Course Category',
    #                                   queryset = CourseCategory.objects.all())
    
    filter_semester = forms.ModelChoiceField(label = 'Semester',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
    section = forms.ModelChoiceField(required = False, empty_label = 'Choose Section',
                                     queryset = Section.objects.none())
    subject = forms.ModelChoiceField(required = False, empty_label = 'Choose Subject',
                                     queryset = Subject.objects.none())
    start_date = forms.DateField(required = False, label = 'From', widget=forms.DateInput(attrs = {'type':'date','class':''}))
    end_date = forms.DateField(required = False,label = 'To',widget=forms.DateInput(attrs = {'type':'date','class':''}))
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))
    
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        subject = self.fields['subject']
        filter_semester = self.fields['filter_semester']
        # course_category = self.fields['course_category']
        # course_category.queryset = user.staff.course.all()
        filter_semester.queryset = user.semester_set.all()
        subject.queryset = user.subject_set.all()

class ContentFilterForm(forms.Form):
   
    
    # if course_category_instance not in CourseCategory.objects.filter(course_name__in = ['Plus-Two','Bachelor','Master']):
    #     print("Error")
    # else:
    #     print("::else part")
    course = forms.ModelChoiceField(required = False, empty_label = 'Choose Course',
                                       queryset = Course.objects.all())
        
    semester = forms.ModelChoiceField(label = '',required = False, empty_label = 'Choose Class',
                                      queryset = Semester.objects.all(),widget=forms.Select(attrs = {'hidden':''}))
    section = forms.ModelChoiceField(required = False, empty_label = 'Choose Section',
                                     queryset = Section.objects.all())
    subject = forms.ModelChoiceField(empty_label = 'Choose Subject',
                                     queryset = Subject.objects.none())
    teacher = forms.ModelChoiceField(required = False,empty_label = 'Choose Teacher',
                                     queryset = Staff.objects.all())
    start_date = forms.DateField(required = False, label = 'From', widget=forms.DateInput(attrs = {'type':'date','class':''}))
    end_date = forms.DateField(required = False,label = 'To',widget=forms.DateInput(attrs = {'type':'date','class':''}))
    
    def __init__(self, semester_id, *args, **kwargs):
        super(ContentFilterForm,self).__init__(*args, **kwargs)
        
        section = kwargs.pop('section', None)
        subject = kwargs.pop('subject', None)
        course = kwargs.pop('course', None)
        semester = Semester.objects.get(pk = semester_id)
        if semester.course is None:
            self.fields['course'].widget = forms.HiddenInput()
        self.fields['course'].queryset = Course.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))
        self.fields['section'].queryset = Section.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))
        self.fields['subject'].queryset = Subject.objects.filter(semester =  get_object_or_404(Semester , pk = semester_id))
        # self.fields['teacher'].queryset = SemesterTeacher.objects.filter(semester =  get_object_or_404(Semester , pk = semester_id))
         

class SectionWiseFilter(forms.Form):
    # course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
    #                                   queryset = CourseCategory.objects.all())
    
    # semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
    #                                   queryset = Semester.objects.none())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',
                                     queryset = Section.objects.none())
 
    def __init__(self, semester_id, *args, **kwargs):
        super(SectionWiseFilter,self).__init__(*args, **kwargs)
        
        section = kwargs.pop('section', None)
        semester = Semester.objects.get(pk = semester_id)
        self.fields['section'].queryset = Section.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))

class SubjectWiseFilter(forms.Form):
    # course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
    #                                   queryset = CourseCategory.objects.all())
    
    # semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
    #                                   queryset = Semester.objects.none())
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',
                                     queryset = Subject.objects.none())
 
    def __init__(self, semester_id, *args, **kwargs):
        super(SubjectWiseFilter,self).__init__(*args, **kwargs)
        
        subject = kwargs.pop('subject', None)
        semester = Semester.objects.get(pk = semester_id)
        self.fields['subject'].queryset = Subject.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))



class TeacherSyllabusFilterForm(forms.Form):
    subject = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Subject',
                                     queryset = SubjectTeacher.objects.all())

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        subject = self.fields['subject']
        subject.queryset = user.subjectteacher_set.all()
     

class EnotesFilterForm(forms.Form):
       
    category_choices = (
        ('', 'Choose E-Note Category'),
        ('Subject Notes','Subject Notes'),
        ('Extra Notes','Extra Notes'))


    # section = forms.ModelChoiceField(required = False,label = '', empty_label = 'Choose Section',
    #                                  queryset = Section.objects.all())
    

    subject = forms.ModelChoiceField(empty_label = 'Choose Subject',
                                     queryset = Subject.objects.none())

    category=forms.ChoiceField(choices=category_choices,
                        )
    start_date = forms.DateField(required = False, label = 'From', widget=forms.DateInput(attrs = {'type':'date','class':''}))
    end_date = forms.DateField(required = False,label = 'To',widget=forms.DateInput(attrs = {'type':'date','class':''}))

    
    def __init__(self,semester = None, user = None, *args, **kwargs):
        super(EnotesFilterForm,self).__init__(*args, **kwargs)
        
        subject = kwargs.pop('subject', None)
        if user.groups.filter(name='Teacher'):
            print("satecher:::")
            self.fields['subject'].queryset = user.subjectteacher_set.all()
        if user.groups.filter(name='Student'):
            self.fields['subject'].queryset = Subject.objects.filter(semester =  user.student.semester)
        if user.groups.filter(name='Super-Admin') or user.is_superuser:
            self.fields['subject'].queryset = Subject.objects.filter(semester =  get_object_or_404(Semester , pk = semester))
    
         

         

class SubjectAssignFilterForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    filter_course = forms.ModelChoiceField(label= '',empty_label = 'Choose Course',
                                      queryset = Course.objects.all())
    
    filter_semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section',
                                     queryset = Section.objects.none())
 
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))
class SemesterAssignFilterForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    filter_course = forms.ModelChoiceField(label= '',empty_label = 'Choose Course',
                                      queryset = Course.objects.all())
    
 


class SyllabusSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
  
 
    # group=forms.ChoiceField(required = False, label = '',choices=faculty_choices,
    #                       widget=forms.Select(attrs = {'hidden':''}))


class DynamicSyllabusForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',empty_label = 'Choose Course Category',
                                      queryset = CourseCategory.objects.all())
    
    
    semester = forms.ModelChoiceField(label= '',empty_label = 'Choose Class',
                                      queryset = Semester.objects.none())
    
    
    # def __init__(self, semester_id, *args, **kwargs):
    #         super(ContentFilterForm,self).__init__(*args, **kwargs)
        
    #     # course = kwargs.pop('course', None)
    #     semester = Semester.objects.get(pk = semester_id)
    #     if semester.course is None:
    #         self.fields['course'].widget = forms.HiddenInput()
    #     self.fields['course'].queryset = Course.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))
    #     self.fields['section'].queryset = Section.objects.filter(semester = get_object_or_404(Semester , pk = semester_id))
    #     # self.fields['subject'].queryset = Subject.objects.filter(semester =  get_object_or_404(Semester , pk = semester_id))
    

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
        fields = ('course_category','course','routine_file','semester','section',)
    

class SubjectSearchForm(forms.Form):
    subject = forms.ModelChoiceField(label = '',empty_label="Select Subject", queryset = Subject.objects.all())
    
    def __init__(self, request, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        subject = self.fields['subject']
        subject.queryset = subject.queryset.filter(staff_user__subject = request.user.student.subject)
        

class RoutineSearchForm(forms.Form):
    # course_category = forms.ModelChoiceField(label = '',empty_label="Course Category",queryset = CourseCategory.objects.all())
    # filter_course = forms.ModelChoiceField(label = '',empty_label="Course",required = False, queryset = Course.objects.all())
    filter_semester = forms.ModelChoiceField(label = '',empty_label="Select Semester", queryset = Semester.objects.all())
    section = forms.ModelChoiceField(label = '',empty_label="Select Section", queryset = Section.objects.none())
   
    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        filter_semester = self.fields['filter_semester']
        filter_semester.queryset = user.semester_set.all()
        # filter_semester.queryset = user.semesterteacher_set.all()
# class AdminRoutineSearchForm(forms.Form):
#     course_category = forms.ModelChoiceField(label = '',empty_label="Course Category",queryset = CourseCategory.objects.all())
#     filter_course = forms.ModelChoiceField(label = '',empty_label="Course",required = False, queryset = Course.objects.all())
#     filter_semester = forms.ModelChoiceField(label = '',empty_label="Select Semester", queryset = Semester.objects.all())
#     section = forms.ModelChoiceField(label = '',empty_label="Select Section", queryset = Section.objects.none())
    
   
   
        
        
class SubjectForm(forms.ModelForm):
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    semester = forms.ModelChoiceField(queryset = Semester.objects.all())
    course = forms.ModelChoiceField(required = False, queryset = Course.objects.all())
    subject_name = forms.CharField(required = True, widget=forms.TextInput(
        attrs={'placeholder': 'Enter Your Subject Name'}))
    # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
    #     attrs={'placeholder': 'Enter Semester Value'}))
    description = forms.CharField(required=False, widget=forms.Textarea(
        attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))
    class Meta:
        model=Subject
        fields = ('course_category','course','semester','subject_name','subject_code','description')
 


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
        fields = ('course_category','course','name','description')
        
class ClassSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',
                                      empty_label = '---Click Here To  Filter Class---', 
                                      queryset = CourseCategory.objects.all())
    filter_course = forms.ModelChoiceField(required = False, label= '',
                                      empty_label = '---Click Here To  Filter Course---', 
                                      queryset = Course.objects.none())
    
    
class SectionSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',
                                      empty_label = '--- Filter Course Category ---', 
                                      queryset = CourseCategory.objects.all())
    filter_course = forms.ModelChoiceField(required = False, label= '',
                                      empty_label = '--- Filter Course ---', 
                                      queryset = Course.objects.none())
    filter_semester = forms.ModelChoiceField(label= '',
                                      empty_label = '--- Filter Class ---', 
                                      queryset = Semester.objects.none())
     

class SubjectSearchForm(forms.Form):
    course_category = forms.ModelChoiceField(label= '',
                                      empty_label = '---Filter Course Category---', 
                                      queryset = CourseCategory.objects.all())
    filter_course = forms.ModelChoiceField(label= '',required = False,
                                      empty_label = '--- Filter Course---', 
                                      queryset = Course.objects.none())
    filter_semester = forms.ModelChoiceField(label= '',
                                      empty_label = '---Filter Class---', 
                                      queryset = Semester.objects.none())
                                      
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
        
# class SectionForm(forms.ModelForm):#for a-level
#     course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.exclude(course_name__in = ['School']), widget=forms.RadioSelect())
#     name = forms.CharField(required = False, widget=forms.TextInput(
#         attrs={'placeholder': 'Enter Your Class Name'}))
#     # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
#     #     attrs={'placeholder': 'Enter Semester Value'}))
#     description = forms.CharField(required=False, widget=forms.Textarea(
#         attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
#     class Meta:
#         model = Semester
#         fields = ('course_category','name','description')
        
        
# class SectionForm(forms.ModelForm):#for a-level
#     course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
#     name = forms.CharField(required = False, widget=forms.TextInput(
#         attrs={'placeholder': 'Enter Your Class Name'}))
#     # semester_value = forms.IntegerField(required = False, widget=forms.NumberInput(
#     #     attrs={'placeholder': 'Enter Semester Value'}))
#     description = forms.CharField(required=False, widget=forms.Textarea(
#         attrs={'rows': 2, 'cols': 10, "placeholder": " Enter  Course Description", }))

   
#     class Meta:
#         model = Semester
#         fields = ('course_category','name','description')
        
class SectionForm(forms.ModelForm):
 
    course_category = forms.ModelChoiceField(queryset = CourseCategory.objects.all(), widget=forms.RadioSelect())
    course = forms.ModelChoiceField(required = False, queryset = Course.objects.all())
    semester = forms.ModelChoiceField(queryset = Semester.objects.all())
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
        fields = ['course_category','course','semester','section_name','capacity','description']
     

            
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
    


class StudentSearch(FilterForm):
    course_category = forms.ModelChoiceField(required = False,label= '',queryset = CourseCategory.objects.all(),empty_label = 'Select Course Category')
    filter_course = forms.ModelChoiceField(label= '',required = False, queryset = Course.objects.all(),empty_label = 'Select Course')
                   
    filter_semester = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Class', queryset = Semester.objects.all())
    section = forms.ModelChoiceField(required = False, label= '',empty_label = 'Choose Section', queryset = Section.objects.all()) 
    
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user.groups.filter(name='Teacher'):
            course_category = self.fields['course_category']
            course_category.queryset = user.staff.courses.all()
        if user.is_superuser or  user.groups.filter(name='Super-Admin'):
            course_category = self.fields['course_category']
            course_category.queryset = CourseCategory.objects.all()