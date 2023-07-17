from django.db import models
import datetime
from django.utils import timezone
from student_management_app.models import Student, Subject, Semester,CourseCategory
from django.db.models.signals import post_save
from django.dispatch import receiver
from student_management_app.models import   Student
from django.utils.translation import gettext_lazy as _
from django.db import transaction

YEAR_CHOICES = [(r,r) for r in range(1990, datetime.date.today().year+1)]

class Term(models.Model):
    exam_choices = [
        ('Unit','Unit Test'),
        ('Term', 'Terminal Examination')
    ]
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    # term_id = models.CharField(max_length=30, primary_key=True)
    term_id = models.BigAutoField(auto_created=True, primary_key=True)
    year = models.IntegerField(choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    term_name = models.CharField(max_length=25)
    type = models.CharField(max_length=5, choices= exam_choices, default = 'Unit')
    full_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=40)
    start_date = models.DateField(null = True, blank=True)
    end_date = models.DateField(null = True, blank=True)
    exam_centre = models.CharField(max_length=30,null = True, blank=True)
    is_published = models.BooleanField(default = False)
    # publish_date = models.DateField(auto_now_add = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
   
    
    def get_latest(self):
        return self.latest('start_date')
    
    def __str__(self):
        return f'{self.term_name}-{self.year}({self.course_category})'



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
    # semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null = True)
    exam_type = models.CharField(max_length=5, choices= exam_choices, default = 'Unit')
    exam_format = models.CharField(max_length=50,choices  = format_choices )
    date = models.DateField(null=True, blank = True)
    time = models.TimeField(null=True, blank = True)
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
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE,null=True, blank=True)
    semester = models.ForeignKey(Semester, verbose_name = 'Class', on_delete=models.CASCADE,null = True, blank=True)
    
    term = models.ForeignKey(Term, on_delete=models.CASCADE,null=True, blank=True)
    exam_id = models.ForeignKey(Exams, on_delete=models.CASCADE,null=True, blank=True)
    application_id = models.ForeignKey(application_form, on_delete=models.CASCADE,null=True, blank=True)
    marks = models.FloatField(default=0)
    grade = models.CharField(max_length=6, choices=GRADE_OPTIONS, default='U')
    passed = models.BooleanField()
    exam_type = models.BooleanField(null=True, blank=True) #True=Regular, False=Chance
    is_absent = models.BooleanField(default=False)
    rank = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.student.student_user.full_name# + " " + self.exam_id.exam_title
    
    def save(self, *args, **kwargs):
        self.passed = True if self.marks>=self.term.pass_marks else False

        # level = self.application_id.student.semester.level

        # if self.exam_id.exam_type == 'Term':
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
        # else:
        #     if level == 'AS':
        #         self.grade='A'
        #     else:
        #         self.grade='A*'

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
    
# signals.py



@receiver(post_save, sender=Term)
def create_exams_and_application_forms(sender, instance, created, **kwargs):
    if created:
        '''Automatically create exam for all subjects for school(one to class ten only)'''
      
        exam_format = 'Close Book'
        print(instance.type,"::::::::::::::::::::::::::::::::::::::::::::::")
        if instance.type == 'Unit':
            pass_marks = 25
            full_marks = 10
        if instance.type == 'Term':
            pass_marks = 40
            full_marks = 100
        # print(instance.term_name,instance.subject__pk)
        '''Automatically creating exam for all the subjects when admin create term from 1 to 10 as exam type are almost similar'''
        # school_subjects = Subject.objects.filter(course_category = CourseCategory.objects.get(course_name = 'School'))
        subjects = Subject.objects.all()#filter(course_category = CourseCategory.objects.get(course_name = 'School'))

        for subject in subjects:
            exam_instance = Exams(
                exam_id = f'{instance.term_name}.{subject.pk}.{subject.semester.pk}',

                term = instance,
                exam_title = f'{subject.subject_name}.{instance.term_name}.{subject.semester.name}',
                semester = Semester.objects.get(pk  = subject.semester.pk),
                subject_id = Subject.objects.get(pk = subject.pk), 
                exam_format = exam_format, 
                pass_marks= pass_marks,
                full_marks = full_marks,
                created_at = timezone.now()
                
                
            )
            exam_instance.save()
        # '''Automatically create application form'''
        # students = Student.objects.select_related('student_user').all()
        # term_id = instance.pk

        # application_forms_to_create = []
        # for student in students:
        #     student_username = student.student_user.username
        #     application_id = f'{term_id}.{student_username}' 

        #     application_form_obj = application_form(
        #         application_id=application_id,
        #         term=instance,
        #         student=student,
        #         semester=student.semester
        #     )

        #     application_forms_to_create.append(application_form_obj)

        # with transaction.atomic():
        #     application_form.objects.bulk_create(application_forms_to_create)

# ----------------------or 

        # students = Student.objects.all()#.values('student_user__username', 'pk', 'semester')

        # for student in students:
        #     term_id = instance.pk
        #     student_username = student.student_user.username
        #     application_id = f'{term_id}.{student_username}' 
        #     application_form.objects.get_or_create(application_id = application_id, term=instance, student=student, semester=student.semester)



























# exams = []
#    app_obj = application_form(application_id=app_id, student=student, term=term, semester=student.semester)

#     if (application_form.objects.filter(application_id=app_id).exists()):

#         while(i<count):
#             exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
#             i+=1
    
#         print(exams)
#         for item in exams:
#             if item not in app_obj.exam.all():
#                 print(str(item))
#                 '''I make this passed = true as I dont want admin to verify for appliation form '''
#             app_obj.exam.add(item, through_defaults={'exam_type':True, 'passed':True})#
        
#         app_obj.save()

#         messages.success(request, 'Application successful. <a href="printapplicationform">Test link</a><br>Or access the page from sidebar.', extra_tags='safe')
#         return HttpResponseRedirect(reverse('home'))
#     else:
#         app_obj.save()

#         while(i<count):
#             exams.append(get_object_or_404(Exams, pk=request.POST[str(i)]))
#             i+=1
    
#         for item in exams:
#             app_obj.exam.add(item, through_defaults={'exam_type':True, 'passed':True})
        
#         app_obj.save()
        
#         messages.success(request, 'Application successful. Print form <a href="printapplicationform">here</a>', extra_tags='safe')
#         return HttpResponseRedirect(reverse('home'))
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
