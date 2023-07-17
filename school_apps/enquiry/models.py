from django.db import models
from student_management_app.models import Course

from io import StringIO

# Create your models here.


class Enquiry(models.Model):
    STATUS = [
        ("ENQ", "Enquired"),
        ("APL_SENT", "Application Sent"),
        ("APL", "Applied"),
        # ("ENT_PASSED", "Entrance Exam passed"),
        # ("INT_PASSED", "Interview passed"),
        # ("ENR", "Enrolled"),
        ("DRP", "Dropped"),
    ]

    RESULT = [("PASS", "Passed"), ("FAIL", "Failed"),
              ("NA", "Not appeared yet")]

    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60, blank=True)
    home_contact = models.CharField(max_length=60, blank=True)
    mobile_no = models.CharField(max_length=60)
    email = models.EmailField(unique=True)
    discovery_method = models.CharField(
        verbose_name="How did you know about this college?",
        max_length=250,
        blank=True)
    called = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100,
        choices=STATUS,
        blank=True,
        default="ENQ")
    application_sent = models.BooleanField(default=False)

    entrance_marks = models.IntegerField(null=True, blank=True)
    entrance_result = models.CharField(
        max_length=10, choices=RESULT, default="NA")
    entrance_result_sent = models.BooleanField(default=False)
    interview_result = models.CharField(
        max_length=10, choices=RESULT, default="NA")
    interview_result_sent = models.BooleanField(default=False)

    enquiry = models.CharField(max_length=250, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name + " " + self.email


class Application(models.Model):
    STATUS = [
        ("APL", "Applied"),
        ("ENT_PASSED", "Entrance Exam passed"),
        ("INT_PASSED", "Interview passed"),
        ("ENR", "Enrolled"),
        ("DRP", "Dropped"),
    ]

    RESULT = [("PASS", "Passed"), ("FAIL", "Failed"),
              ("NA", "Not appeared yet")]
    SEX_CHOICES = [("M", "Male"), ("F", "Female"), ("O", "Others")]

    enquiry = models.OneToOneField(
        Enquiry, on_delete=models.CASCADE, null=True, blank=True
    )
    name = models.CharField(max_length=100)
    photo = models.ImageField(
        upload_to="application/student",
        null=True,
        blank=True)
    dob = models.DateField()
    sex = models.CharField(max_length=100, choices=SEX_CHOICES)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    # temporary_address = models.JSONField()
    # permanent_address = models.JSONField()
    temporary_address = models.CharField(max_length=250)
    permanent_address = models.CharField(max_length=250)
    email = models.EmailField(unique=True)
    home_phone = models.CharField(max_length=15, null=True, blank=True)
    contact_no = models.CharField(max_length=15)
    # education_history = models.JSONField()
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, null=True, blank=True)
    father_office = models.CharField(max_length=100, null=True, blank=True)
    father_phone = models.CharField(max_length=20, null=True, blank=True)
    father_email = models.EmailField(null=True, blank=True)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100, null=True, blank=True)
    mother_office = models.CharField(max_length=100, null=True, blank=True)
    mother_phone = models.CharField(max_length=20, null=True, blank=True)
    mother_email = models.EmailField(null=True, blank=True)
    guardian_name = models.CharField(max_length=100)
    guardian_address = models.CharField(max_length=100)
    guardian_occupation = models.CharField(
        max_length=100, null=True, blank=True)
    guardian_office = models.CharField(max_length=100, null=True, blank=True)
    guardian_phone = models.CharField(max_length=20, null=True, blank=True)
    guardian_email = models.EmailField(null=True, blank=True)
    additional_fields = models.JSONField(null=True, blank=True)

    discovery = models.TextField(
        verbose_name="How did you know about this college?",
        null=True,
        blank=True)

    status = models.CharField(
        max_length=100,
        choices=STATUS,
        blank=True,
        default="APL")
    entrance_marks = models.IntegerField(null=True, blank=True)
    entrance_result = models.CharField(
        max_length=10, choices=RESULT, default="NA")
    entrance_result_sent = models.BooleanField(default=False)
    interview_result = models.CharField(
        max_length=10, choices=RESULT, default="NA")
    interview_result_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.name + " " + self.email
