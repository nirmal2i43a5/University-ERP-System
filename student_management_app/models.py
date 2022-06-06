import datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.shortcuts import get_object_or_404
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField
from ckeditor.fields import RichTextField
from django.contrib.auth.models import Group
from school_apps.transports.models import Transport
from simple_history.models import HistoricalRecords

# from PIL import Image
# for qrcode
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
# from simple_history.models import HistoricalRecords
# barcode
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File


gender_choice = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Third Gender', 'Third Gender')
)


school_classes_choices = (
        ('NURSERY','NURSERY'),
        ('LKG','LKG'),
        ('UKG','UKG'),
        ('ONE','ONE'),
        ('TWO','TWO'),
        ('THREE','THREE'),
        ('FOUR','FOUR'),
        ('FIVE','FIVE'),
        ('SIX','SIX'),
        ('SEVEN','SEVEN'),
        ('EIGHT','EIGHT'),
        ('NINE','NINE'),
        ('TEN','TEN'),
        
    )

# PLUS_TWO_CHOICES = [
#         ('AS', 'Advanced Subsidiary (AS)'),
#         ('AL', 'Advanced Level (AL)'),
#         ('PA', 'Passed out')
#         ]

ALEVEL_CHOICES = [
        ('AS', 'Advanced Subsidiary (AS)'),
        ('AL', 'Advanced Level (AL)'),
        ('PA', 'Passed out')
        ]

bachelor_semester_choices = (
        ('First','First'),
        ('Second','Second'),
        ('Third','Third'),
        ('Fourth','Fourth'),
        ('Fifth','Fifth'),
        ('Sixth','Sixth'),
        ('Seventh','Seventh'),
        ('Eight','Eight'),
    )
master_semester_choices = (
        ('First','First'),
        ('Second','Second'),
        ('Third','Third'),
        ('Fourth','Fourth'),
    )


YEAR_CHOICES = []
for r in range(2010, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

        
class Department(models.Model):
    name = models.CharField(_("Department Name"), max_length=50)
    # description = models.TextField(blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField(verbose_name="Branch name:", max_length=50)

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):  # use this for extending deafult django auth system
    full_name = models.CharField(max_length=255)
    user_type = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
    # password = models.CharField(_('password'), max_length=128, null = True)

    class Meta:
        db_table = 'tbl_Customuser'
        verbose_name = _("customuser")
        verbose_name_plural = _("customusers")

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SessionYear(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()

    class Meta:
        db_table = 'tbl_Sessionyear'

    def __str__(self):

        return f'{str(self.session_start_year)} To {str(self.session_end_year)}'



class CourseCategory(models.Model):  # i also want to see subject for particular course
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.course_name
    

    
class AdminUser(models.Model):
    # linking main auth model to admin which assists to relate to admin table with its id.Do same for staffs and students
    admin_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, choices=gender_choice, default='Male', blank=True)
    religion = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    join_date = models.DateField(null=True,blank = True)
    image = models.ImageField(upload_to='admin_images', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Adminuser'
        verbose_name = _("adminuser")
        verbose_name_plural = _("adminusers")
        permissions = (
            ("view_admin_profile", "Can View Profile"),
            ("add_admin_document", "Can Add Document"),
            ("edit_admin_document", "Can Edit Document"), 
            ("delete_admin_document", "Can Delete Document"),
         
        )
        

    def __str__(self):
        return self.admin_user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    
class Course(models.Model):  # i also want to see subject for particular course
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    course_name = models.CharField(max_length=255,null = True)
    course_code = models.CharField(max_length=50, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,null = True, blank=True)
    course_description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Course'
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.course_name



class Staff(models.Model):  
    courses = models.ManyToManyField(CourseCategory, max_length=100)
    staff_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField( max_length=20, choices=gender_choice, default='Male')
    religion = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=30)
    join_date = models.DateField(null=True,blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)
    status = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Staff'
        verbose_name = _("staff")
        verbose_name_plural = _("staffs")
        
        permissions = (
            ("view_teacher_profile", "Can View Profile"),
            ("add_teacher_document", "Can Add Document"),
            ("edit_teacher_document", "Can Edit Document"), 
            ("delete_teacher_document", "Can Delete Document"),
         
        )

    def __str__(self):
        return self.staff_user.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # def get_subjects(self):
    #     customuser_teacher = CustomUser.objects.filter(user_type = Group.objects.get(name = 'Teacher')).get(id = teacher_id)
    #     subjects = customuser_teacher.subject_set.all()
    #     return subjects

    


# class dropdown(models.Model):
#     name:
#     values:

class ExtraUser(models.Model):  # this all other user like driver accountant and so on
    extra_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null = True)
    role = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    dob = models.DateField(null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=gender_choice, default='Male')
    religion = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=30, blank=True)
    address = models.CharField(max_length=255, blank=True)
    join_date = models.DateField(null=True)
    image = models.ImageField(upload_to='user_images', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Extrauser'
        verbose_name = _("extrauser")
        verbose_name_plural = _("extrausers")
        permissions = (
            ("view_extrauser_profile", "Can View Profile"),
            ("add_extrauser_document", "Can Add Document"),
            ("edit_extrauser_document", "Can Edit Document"), 
            ("delete_extrauser_document", "Can Delete Document"),   
         
        )

    def __str__(self):
        return self.extra_user.full_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#new added model
# class Alevel_level(models.Model):



class Semester(models.Model):
 
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    name = models.CharField(max_length=100)#for school classes
    level = models.CharField(max_length=20, choices=ALEVEL_CHOICES, default='AS',null = True,blank = True)
    bachelor_semester = models.CharField(_("Course Name"),max_length=100,null = True, blank = True)
    master_semester = models.CharField(_("Course Name"),max_length=100,null = True, blank = True)
    semester_value = models.IntegerField(null=True, blank=True)
    # staff_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null = True, blank = True)
    description = models.TextField(blank=True)
    status = models.BooleanField(default=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Semester'
        verbose_name = _("semester")
        verbose_name_plural = _("semesters")
        ordering = ('pk',)


    def __str__(self):
        
        school_course_category = get_object_or_404(CourseCategory,course_name = 'School')
        a_level_course_category = get_object_or_404(CourseCategory,course_name = 'A-Level')
        bachelor_course_category = get_object_or_404(CourseCategory,course_name = 'Bachelor')
        master_course_category = get_object_or_404(CourseCategory,course_name = 'Master')
        
        if self.course_category == school_course_category:
               return f'{self.name}'
           
        if self.course_category == a_level_course_category:
           return f'{self.name}'
            
        if self.course_category == bachelor_course_category:
            return f'{self.name}'
        
        if self.course_category == master_course_category:
            return f'{self.name}'

    



class Subject(models.Model):

    faculty_choices = (
        ('Science',' Science'),
        ('Non-Science',' Non-Science')
    )
    
    
    subject_code = models.CharField(max_length=50, primary_key = True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    # semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    faculty = models.CharField(_('Group'), max_length=50,choices = faculty_choices,blank = True)
    bachelor_semester = models.CharField(_('Semester'),max_length=100,choices = bachelor_semester_choices,null = True, blank = True)
    master_semester = models.CharField(_('Semester'),max_length=100,choices = master_semester_choices,null = True, blank = True)
    subject_name = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null= True, blank=True)
    staff_user = models.ManyToManyField(CustomUser, through='SubjectTeacher',  blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Subject'
        verbose_name = _("subject")
        verbose_name_plural = _("subjects")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject_name
    # def __str__(self):
    #     return f'{self.semester} : {self.subject_name} : ' + ' , '.join([str(teacher) for teacher in self.staff_user.all()])
    
    @property
    def get_teachers(self):
        return ', '.join(str(teacher) for teacher in self.staff_user.all())


class Section(models.Model):
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    section_name = models.CharField(max_length=100)
    capacity = models.IntegerField(null = True, blank = True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null = True)
    staff = models.ForeignKey(CustomUser, on_delete=models.CASCADE,null = True, blank = True)
    category = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    subject = models.ManyToManyField(Subject)
    history = HistoricalRecords()
    
    class Meta:
        db_table = 'tbl_Section'
        verbose_name = _("section")
        verbose_name_plural = _("sections")
    
    def __str__(self):
        return f'{self.semester} : {self.section_name}'



class SubjectTeacher(models.Model):
    subject = models.ForeignKey(Subject, verbose_name=_("Subject"), on_delete=models.CASCADE)
    teacher = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,null = True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['subject', 'section'], name = 'unique_subject_teacher_section')
        ]
    
    def __str__(self):
        return f'{self.subject.subject_name}:{self.teacher}'
    
    
class OptionalSubject(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=255)
    subject_code = models.CharField(max_length=50, default='XXX', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tbl_Optionalsubject'
        verbose_name = _("optionalsubject")
        verbose_name_plural = _("optionalsubjects")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.subject_name


class Parent(models.Model):
    # --gci field
    home_phone = models.CharField(max_length=30,null = True, blank=True)
    father_name = models.CharField(max_length=100, null = True, blank=True)#full_namei.e customuser retrieve from this is placed in father name
    father_phone = models.CharField(max_length=30,null = True, blank=True)
    mother_name = models.CharField(max_length=100,null = True, blank=True)
    mother_phone = models.CharField(max_length=30,null = True, blank=True)
    local_guardian_name = models.CharField(max_length=100,null = True, blank=True)
    local_guardian_phone = models.CharField(max_length=30,null = True, blank=True)
    
    # ------other extra field 
    father_profession = models.CharField(max_length=255,null = True, blank=True)
    father_email = models.EmailField(null=True, blank=True)
    father_profession = models.CharField(max_length=255,null = True, blank=True)
    father_office = models.CharField(max_length = 100, null=True, blank=True)
    mother_profession = models.CharField(max_length=255,null = True, blank=True)
    mother_email = models.EmailField(null=True, blank=True)
    mother_office = models.CharField(max_length = 100, null=True, blank=True)
    address = models.CharField(max_length=255,null = True, blank=True)
    image = models.ImageField(upload_to='parent_images', null=True, blank=True)
    status = models.BooleanField(default=True)
    parent_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_Parent'
        verbose_name = _("parent")
        verbose_name_plural = _("parents")
        
        permissions = (
            ("view_parent_profile", "Can View  Profile"),
            ("add_parent_document", "Can Add Document"),
            ("edit_parent_document", "Can Edit Document"), 
            ("delete_parent_document", "Can Delete Document"),
         
        )

    # def __str__(self):
    #     return self.parent_user.full_name


#THis is for student union college union group
class StudentGroup(models.Model):
    name = models.CharField(max_length=250, blank=True,verbose_name = 'Student Union Name', help_text='This is Student  Union GrouP')
    class Meta:
        db_table = 'tbl_Studentgroup'
        verbose_name = _("studentgroup")
        verbose_name_plural = _("studentgroups")

    def __str__(self):
        return self.name




# class SectionSubject(models.Model):
#     section = models.ForeignKey(Section, on_delete=models.CASCADE)
#     subject = models.ForeignKey(SubjectTeacher, on_delete=models.CASCADE)
    
    # class Meta:
    #     db_table = 'tbl_SectionSubject'
    #     verbose_name = _("SectionSubject")
    #     verbose_name_plural = _("SectionSubjects")
        
    # def __str__(self):
    #     return f'{self.section.section_name}:{self.subject}'
    
class Student(models.Model):
    blood_group_choices = (
        ('', 'Select Blood Group'), ('A+', 'A+'), ('A-',
                                                   'A-'), ('B+', 'B+'),  ('B-', 'B-'),
        ('O+', 'O+'),  ('O-', 'O-'), ('AB+', 'AB+'),  ('AB-', 'AB-'),
    )
    shift = (
        ('Morning','Morning'),
          ('Day','Day')
    )
    status_choices = (
        ('Running','Running'),('In Active','In Active')
    )
    faculty_choices = (
        ('Science','Science'),
        ('Non-Science','Non-Science')
    )
    category_choices = (
        ('A-Level','A-Level'),('z','Bachelor'),('Master','Master')
    )
        

    # id = models.CharField(max_length=100, primary_key = True)#doing this give error for : foreign key mismatch - "courses_application_form" referencing "tbl_Student" 
    # s_no = models.CharField(max_length=10, null=True,blank=True)
    join_year = models.CharField(_('Join Year'),max_length = 50, default=datetime.datetime.now().year, null = True,blank = True)#this is same as batch
    stu_id = models.CharField(max_length=50,unique=True)
    roll_no = models.CharField(max_length=10,null=True,blank=True)
    full_name = models.CharField(max_length=50,null = True, blank = True)
    student_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null = True, blank = True)
    gender = models.CharField(max_length=20, choices=gender_choice,null = True, default='Male')
    shift = models.CharField(max_length=20,  choices=shift,  null=True,blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
    course = models.CharField(max_length=250, null=True,blank=True)
    faculty = models.CharField(max_length=50,choices = faculty_choices,null = True, blank = True)
    # category = models.CharField(max_length=50,choices = category_choices,null = True, blank = True)
    course_category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE,null = True, blank=True)
    program = models.CharField(max_length=250, null=True,blank=True)
    status = models.CharField(max_length=50,choices = status_choices)
    contact = models.CharField(max_length=30, blank=True)
    # guardian = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,null=True, blank=True, related_name = "Student_Parent")
    guardian = models.ForeignKey(Parent, on_delete=models.DO_NOTHING,null=True, blank=True)
    permanent_address = models.CharField(max_length=255, blank=True)
    temporary_address = models.CharField(max_length=255, blank=True)
    dob = models.DateField(null=True, blank=True)
    blood_group = models.CharField(max_length=25, choices=blood_group_choices, blank=True)
    optional_subject = models.ForeignKey(Subject,related_name = 'student_optional_subject', on_delete=models.CASCADE, null=True)
    see_gpa = models.CharField(max_length = 50, blank=True, null=True)
    previous_school_name = models.CharField(max_length=100, null=True,blank=True)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True)
    image = models.ImageField( upload_to='student_images', null=True, blank=True)
    barcode = models.ImageField( upload_to='student_barcodes/', blank=True)
    qr_code = models.ImageField( upload_to='student_Qrcodes/', blank=True)
    
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey( Subject, on_delete=models.CASCADE, null=True, blank=True)#I am using attendance based on subject
    
    # ---------------------------------------------extra field--------------------------------------------------------
    bachelor_course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)#this is for which college degree link mba, bca ,etc

    register_no = models.CharField(max_length=250, unique=True, null=True,blank=True)
    religion = models.CharField(max_length=100,null=True, blank=True)
    remarks = models.CharField(max_length=255,null=True, blank=True)
    extra_curricular_activities = models.CharField(max_length=255, blank=True)
    group = models.ForeignKey( StudentGroup, on_delete=models.CASCADE, null=True, blank=True)#for college group union
    session_year = models.ForeignKey( SessionYear, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=255,null=True, blank=True)
    # country = CountryField(blank_label='(select country)',null=True, blank=True)
    country = models.CharField(max_length = 50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
    
        
    class Meta:
        ordering = ('student_user__full_name',)
        db_table = 'tbl_Student'
        verbose_name = _("student")
        verbose_name_plural = _("students")
        
        permissions = (
            ("view_student_profile", "Can View Profile"),
            ("add_student_document", "Can Add Document"),
            ("edit_student_document", "Can Edit Document"), 
            ("delete_student_document", "Can Delete Document"),
             ("print_student_id_card", "Can Print Id Card"),
            ("student_bulk_upload", "Can Upload Bulk Student Data"),
         
        )

    def __str__(self):
        return f'{self.student_user.full_name} : (Student Id : {self.stu_id}) : ( Roll No : {self.roll_no})'

    
    def student_barcode(self,first_place,  *args, **kwargs):
        COD128 = barcode.get_barcode_class('code128')
        rv = BytesIO()
        code = COD128(f'{first_place}{self.stu_id}', writer=ImageWriter()).write(rv)
        barcode.base.Barcode.default_writer_options['write_text'] = False# this line remove footer text or number
        self.barcode.save(f'{self.student_user.full_name}.png',File(rv), save=False)
        return super().save(*args, **kwargs)
    
    
    def save(self, *args, **kwargs):          # overriding save() 
        # -- for placing digits number in barcode-----------
        student_id = f'{self.stu_id}'
        
        if(len(student_id) == 1):
            first_place = '000000'
            self.student_barcode(first_place)
            
        elif len(student_id) == 2:
            first_place = '00000'
            self.student_barcode(first_place)
            
        elif len(student_id) == 3:
            first_place = '0000'
            self.student_barcode(first_place)
            
        elif len(student_id) == 4:
            first_place = '000'
            self.student_barcode(first_place)
            
        elif len(student_id) == 5:
            first_place = '00'
            self.student_barcode(first_place)
            
        elif len(student_id) == 6:
            first_place = '0'
            self.student_barcode(first_place)
            
        elif len(student_id) == 7:
            first_place = ''
            self.student_barcode(first_place)
            
        # --
      
    
# def upload_location(instance, filename):
#     filebase, extension = filename.split(".")
#     return f'employee documents / {instance.employee_id} . {instance.employee.first_name} {instance.employee.last_name} / {filename}'
         

class DocumentFile(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='document_files')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, null=True)
    extra_user = models.ForeignKey(ExtraUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Documentfile'
        verbose_name = _("documentfile")
        verbose_name_plural = _("documentfiles")

    def __str__(self):
        return self.title





class Complain(models.Model):
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    description = RichTextField()
    attachment = models.FileField(upload_to='Complain_attachment', blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Complain'
        verbose_name = _("complain")
        verbose_name_plural = _("complains")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CertificateTemplate(models.Model):
    theme_choices = (('', 'Choose Template Theme'),
                     ('Theme 1', 'Theme 1'), ('Theme 2', 'Theme 2'))
    title_choices = (
        ('Mr','Mr'),('Mrs','Mrs'),('Miss','Miss'),('Dr','Dr'),('Prof','Prof')
    )
    certificate_number = models.CharField(max_length=50)
    date_of_issue = models.DateField()
    salutations = models.CharField(_("Salutation"), choices = title_choices, max_length=50, null = True, blank = True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True)
    passed_year = models.IntegerField(_('Passed Year'),choices = YEAR_CHOICES,default=datetime.datetime.now().year)
    photo = models.ImageField( upload_to='student_character_certificates_photos', blank=True, null = True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    history = HistoricalRecords()
    # -------------------------------extra field --------------------------
    certificate_name = models.CharField(max_length=250)
    theme = models.CharField(max_length=50, choices=theme_choices)
    main_middle_text = RichTextField()
    top_heading_title = RichTextField(blank=True)
    top_heading_left = RichTextField(blank=True)
    top_heading_middle = RichTextField(blank=True)
    top_heading_right = RichTextField(blank=True)
    footer_left_text = RichTextField(blank=True)
    footer_middle_text = RichTextField(blank=True)
    footer_right_text = RichTextField(blank=True)
    background_image = models.ImageField( upload_to='certificate_template_background', blank=True)

    class Meta:
        db_table = 'tbl_Certificatetemplate'
        verbose_name = _("certificatetemplate")
        verbose_name_plural = _("certificatetemplates")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    role = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    facebook = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    google_plus = models.URLField(max_length=200, blank=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    history = HistoricalRecords()
    # image = models.ImageField(upload_to = 'user_sociallink_images')

    class Meta:
        db_table = 'tbl_Sociallink'
        verbose_name = _("sociallink")
        verbose_name_plural = _("sociallinks")

 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class UserRole(models.Model):
    role = models.CharField(max_length=100)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    
    class Meta:
        db_table = 'tbl_Userrole'
        verbose_name = _("userrole")
        verbose_name_plural = _("userroles")

    def __str__(self):
        return self.role
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)



# >>> a_level = CourseCategory.objects.get(course_name = 'A-Level')
# >>> a_level
# <CourseCategory: A-Level>
# >>> for i in sem:
# ...     i.course_category = a_level
# ...     i.save()
# ... 