from django.db import models

# Create your models here.

class MisSetting(models.Model):
    # id = models.CharField(max_length = 10,primary_key=True,default=1)
    logo = models.ImageField(upload_to = 'logo',null = True,blank=True)
    site_title = models.CharField(max_length=100,null = True,blank=True)
    phone_no =  models.CharField(max_length=20,null = True,blank=True)
    system_email = models.CharField(max_length=100,null = True,blank=True)
    address =  models.CharField(max_length=100,null = True,blank=True)
    academic_year =  models.IntegerField(null = True,blank=True)
    footer =  models.CharField(max_length=100,null = True,blank=True)
    version =  models.CharField(max_length=50,null = True,blank=True)
    
    class Meta:
        db_table = 'tbl_Settings'




