from django.contrib import admin
from student_management_app.models import (Staff,CustomUser,Subject,Staff,Student, DocumentFile,
                                           Course, Parent, ExtraUser, CertificateTemplate,Complain, Semester, SubjectTeacher,SemesterTeacher)

# # # from django.contrib.auth.admin import UserAdmin

# # # admin.site.register(CustomUser, UserAdmin)#using UserAdmin i am able to see some missing functionality to admin site
# admin.site.register(Staff)
admin.site.register(ExtraUser)
admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(Semester)
# # admin.site.register(SectionSubject)
admin.site.register(SubjectTeacher)
admin.site.register(SemesterTeacher)
# # # admin.site.register(DocumentFile)
# admin.site.register(Course)
# # # admin.site.register(CertificateTemplate)
# # # admin.site.register(Complain)

