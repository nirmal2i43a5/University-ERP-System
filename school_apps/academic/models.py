
from django.db.models.fields.related import ManyToManyField
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from student_management_app.models import CustomUser
# from school_apps.courses.models import Semester, Section, Subject
from student_management_app.models import Section, Semester, Subject, Student,CourseCategory,Course
from student_management_system.validators import (validate_file_extension, img_pdf_file_validate_file_extension,img_pdf_doc_validator, pdf_file_validate_file_extension,)


class Syllabus(models.Model):
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null = True, blank=True)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='syllabus',max_length=500,validators=[img_pdf_file_validate_file_extension])
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,null = True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'tbl_Syllabus'
        verbose_name_plural = 'Syllabus'

    def __str__(self):
        return self.title

class Enotes(models.Model):
    category = (('Subject Notes','Subject Notes'),('Extra Notes','Extra Notes'))
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null = True, blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,blank = True,null = True)
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='e-notes',max_length=500,validators=[validate_file_extension])
    note_category = models.CharField(max_length=50,choices = category)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tbl_Enotes'
        verbose_name_plural = 'Syllabus'
    def __str__(self):
            return self.title

class Assignment(models.Model):
    assignment_category = (
    ('Assigned',"Assigned"),('Completed','Completed')
    )
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null = True, blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField()
    # class_id=models.ForeignKey(Class,on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,null = True, blank=True)
    Subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null = True)
    file = models.FileField(upload_to='Assignment_section', blank=True, null=True,max_length=500,validators=[validate_file_extension])
    student = models.ManyToManyField(CustomUser,through = 'Grade')
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null = True,blank=True,related_name='teacher_assignment')
    draft = models.BooleanField(_('Save as Draft'),default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        db_table = 'tbl_Assignment'
        verbose_name_plural = 'Assignment'

    def __str__(self):
        return self.title


class Grade(models.Model):
    assignment_status = (
    ('Assigned',"Assigned"),('Completed','Completed')
    )
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    assignment_status = models.CharField(_("Assignment Category"),choices = assignment_status, 
     max_length=50, default = 'Assigned',null=True, blank=True)#For submitted status by the student
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    # grade = models.PositiveIntegerField(null = True,blank = True)
    # grade_status = models.BooleanField(default=False)#for checking whether assignment is returned to student with points
    # feedback = models.CharField(max_length=255, null=True, blank=True, default="No feedback")
    answer_upload = models.FileField(upload_to = 'Assignment_grades', null=True,max_length=500,validators=[img_pdf_file_validate_file_extension])
    date_submitted = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class AssignmentReturn(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE,related_name='assignment_return')
    grade = models.OneToOneField(Grade, on_delete=models.CASCADE,related_name='grade',blank=True,null=True)
    grade_mark = models.PositiveIntegerField(null = True,blank = True)
    feedback = models.TextField(max_length=255, null=True, blank=True, default="No feedback")
    grade_status = models.BooleanField(default=False)#for checking whether assignment is returned to student with points
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Routine(models.Model):
    year_choices = (
		('2021','2021'),('2022','2022'),('2021','2021'),('2021','2021'),
	)
    
    DAYS_OF_WEEK = (
		('SUNDAY','SUNDAY'),
		('MONDAY','MONDAY'),
  		('TUESDAY','TUESDAY'),
  		('WEDNESDAY','WEDNESDAY'),
  		('THURSDAY','THURSDAY'),
  		('FRIDAY','FRIDAY'),
   		('SATURDAY','SATURDAY'),
	)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null = True, blank=True)
    routine_file = models.FileField(_("Routine"), upload_to='College Routine',max_length=500,validators=[img_pdf_doc_validator])
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,blank=True,null=True)
    # subject = models.ForeignKey(Subject,related_name = 'routine_subject', on_delete=models.CASCADE)
    college_year = models.CharField(max_length=50, choices = year_choices, null=True, blank=True)
    day = models.CharField(max_length=100,choices = DAYS_OF_WEEK, null=True, blank=True)
    # staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    starting_time = models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
    ending_time = models.TimeField(auto_now=False, auto_now_add=False,null=True, blank=True)
    room = models.CharField( max_length=100,null=True, blank=True)
    # course = models.ForeignKey(SectionSubject, on_delete=models.CASCADE)
    # course = models.ForeignKey(Section, on_delete=models.CASCADE, related_name= 'routine_course', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        db_table = 'routine'
        verbose_name_plural = 'Routines'
    
    class Meta:
        db_table = 'tbl_Routine'
        verbose_name_plural = 'Routines'

