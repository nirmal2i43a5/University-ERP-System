from django.db import models
from student_management_app.models import Department, Course
# Create your models here.

class formTemplate(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    elements = models.JSONField()
    css = models.JSONField()
    layouts = models.JSONField()
    settings = models.JSONField()
    is_used = models.BooleanField(default=False)
    # settings = models.TextField()
