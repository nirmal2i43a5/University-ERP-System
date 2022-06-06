
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from student_management_app.models import CustomUser
from simple_history.models import HistoricalRecords


class Notice(models.Model):
    title = models.CharField(max_length=100, blank=True)
    file = models.FileField(upload_to='Notices', null=True, blank=True)
    notice = RichTextField(null=True, blank=True)
    created_by=models.ForeignKey(CustomUser,on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()


    class Meta:
        db_table = 'tbl_notice'
        verbose_name = _("notice")
        verbose_name_plural = _("notices")

    def __str__(self):
        return self.title


class Holiday(models.Model):
    title = models.CharField(max_length=100)
    from_date = models.DateField()
    to_date = models.DateField()
    image = models.FileField(upload_to='holiday_images', null=True, blank=True)
    details = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        db_table = 'tbl_Holiday'
        verbose_name = _("holiday")
        verbose_name_plural = _("holidays")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

