from django.contrib import admin
from .models import SemesterModel, YearModel
# Register your models here.
admin.site.register(SemesterModel)
admin.site.register(YearModel)
