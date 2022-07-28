from django.contrib import admin
from school_apps.academic.models import *
# Register your models here.
admin.site.register(Assignment)
admin.site.register(Grade)
admin.site.register(Syllabus)
admin.site.register(Enotes)
admin.site.register(Routine)