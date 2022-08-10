from django.db import models

# Create your models here.


class SemesterModel(models.Model):
    name = models.CharField( max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class YearModel(models.Model):
    name = models.CharField( max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name