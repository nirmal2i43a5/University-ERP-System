from django.db import models
from student_management_app.models import Department,Course
from io import StringIO

# Create your models here.
    
class Visitor(models.Model):
    REASON_CHOICES =[
                    ("ACA", "Academic"),
                    ("NON", "Non-Academic")]

    name = models.CharField(max_length=60)
    address = models.CharField(max_length=60,blank=True)
    home_contact = models.CharField(max_length=60,null=True, blank=True)
    mobile_no = models.CharField(max_length=60, null=True, blank=True)
    category = models.CharField(max_length=5, default='ACA',verbose_name="Reason", choices=REASON_CHOICES)
    details = models.TextField(null=True, blank=True, verbose_name="Reason for visit")
    department = models.ForeignKey(Department, null=True,blank=True, on_delete=models.CASCADE)
    recipient = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

