from django.contrib import admin
from .models import Term, Exams, application_form, selectedcourses, studentgrades
from student_management_app.models import Subject

# # Register your models here.

admin.site.register(Term)
admin.site.register(Exams)
admin.site.register(Subject)
admin.site.register(selectedcourses)
admin.site.register(studentgrades)
admin.site.register(application_form)
