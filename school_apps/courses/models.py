from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.enums import Choices

from django.db.models.fields import CharField
import datetime
from django.utils import timezone
from student_management_app.models import Student, Staff, Subject, Semester,CourseCategory

from django.utils.translation import gettext_lazy as _
from student_management_app.models import Department

YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Term(models.Model):
    exam_choices = [
        ('Unit','Unit Test'),
        ('Term', 'Terminal Examination')
    ]
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    term_id = models.CharField(max_length=30, primary_key=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    term_name = models.CharField(max_length=25)
    type = models.CharField(max_length=5, choices= exam_choices, default = 'Unit')
    start_date = models.DateField()
    end_date = models.DateField()
    exam_centre = models.CharField(max_length=30)
    is_published = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
    
    def get_latest(self):
        return self.latest('start_date')
    
    def __str__(self):
        return self.term_name
    

class Exams(models.Model):
    format_choices = (
        ('Open Book','Open Book'),    ('Close Book','Closed Book'),
    )

    exam_choices = [
        ('Unit','Unit Test'),
        ('Term', 'Terminal Examination')
    ]
    # course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    exam_id = models.CharField(max_length=100, primary_key=True)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam_title = models.CharField(max_length=100)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null = True)
    exam_type = models.CharField(max_length=5, choices= exam_choices, default = 'Unit')
    exam_format = models.CharField(max_length=50,choices  = format_choices )
    date = models.DateField()
    time = models.TimeField()
    full_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        self.exam_type = self.term.type
        super().save(*args, **kwargs)

    def __str__(self):
        return  f'{self.exam_title}'

class application_form(models.Model):
    application_id = models.CharField( max_length=255,primary_key=True)
    status = models.BooleanField(max_length=3, default=True)  #False = pending
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    exam = models.ManyToManyField(Exams, through='studentgrades')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    application_date = models.DateField(default=timezone.now)
    remarks = models.CharField(max_length=255, default="No Remarks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    
    def save(self, *args, **kwargs):
        self.semester = self.student.semester
        super().save(*args, **kwargs)


class studentgrades(models.Model):
    GRADE_OPTIONS = [
        ('A*','A*'),
        ('A','A'),
        ('B','B'),
        ('C','C'),
        ('D','D'),
        ('E', 'E'),
        ('U', 'U'),
        ('Abs', 'Absent'),
    ]
    exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE)
    application_id = models.ForeignKey(application_form, on_delete=models.CASCADE)
    marks = models.FloatField(default=0)
    grade = models.CharField(max_length=6, choices=GRADE_OPTIONS, default='U')
    passed = models.BooleanField()
    exam_type = models.BooleanField() #True=Regular, False=Chance
    is_absent = models.BooleanField(default=False)
    rank = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.application_id.student.student_user.full_name + " " + self.exam_id.exam_title
    
    def save(self, *args, **kwargs):
        self.passed = True if self.marks>=self.exam_id.pass_marks else False

        level = self.application_id.student.semester.level

        if self.exam_id.exam_type == 'Term':
            if 0<=int(self.marks)<40:
                self.grade='U'
            elif 40<=int(self.marks)<50:
                self.grade='E'
            elif 50<=int(self.marks)<60:
                self.grade='D'
            elif 60<=int(self.marks)<70:
                self.grade='C'
            elif 70<=int(self.marks)<80:
                self.grade='B'
            elif 80<=int(self.marks)<90:
                self.grade='A'
            elif int(self.marks)==-1:
                self.grade='Abs'
            else:
                if level == 'AS':
                    self.grade='A'
                else:
                    self.grade='A*'

        super().save(*args, **kwargs)

class term_ranking(models.Model):
    term=models.ForeignKey(Term, on_delete=models.CASCADE)
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    total_marks = models.IntegerField(default=0)
    rank= models.IntegerField(default=0)


class selectedcourses(models.Model):
    student_id = models.ForeignKey(Student,  on_delete=models.CASCADE, related_name='course_student')
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.student_id.student_user.full_name + " " + self.subject_id.subject_name
    

# class routine(models.Model):

#     DAY_CHOICES = [
#         (1, "Sunday"),
#         (2, "Monday"),
#         (3, "Tuesday"),
#         (4, "Wednesday"),
#         (5, "Thursday"),
#         (6, "Friday"),
#         (0, "Saturday"),
#     ]

#     PERIOD_CHOICES = [(i,i) for i in range (1,9)]
#     semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="routine_semester_fk")
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
#     day = models.IntegerField(choices=DAY_CHOICES)
#     period = models.IntegerField(choices=PERIOD_CHOICES)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(fields = ['semester', 'day', 'period'], name = 'unique_classtime')
#         ]
    
#     def __str__(self) -> str:
#         return str(self.subject) + " semester:" + str(self.semester) + " day:" + str(self.day) + " period:" + str(self.period)

# class Department(models.Model):
#     dept_name = models.CharField(max_length=125)


#     def __str__(self) -> str:
#         return self.dept_name
    
# class course(models.Model):
#     course_name = models.CharField(max_length=100)
#     course_code = models.CharField(max_length=20, unique=True)  #BBA, BCA
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     # intake 

#     def __str__(self) -> str:
#         return self.course_name + " " + self.course_code
