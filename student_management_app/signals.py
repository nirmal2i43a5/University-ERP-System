
"""It receives signal from ready function use in apps.py"""

from school_apps.classroom.models import SemesterModel, YearModel
from student_management_app.models import CustomUser,AdminUser,Staff,Student,Parent,ExtraUser,CourseCategory,Semester
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from school_apps.school_settings.models import MisSetting
from django.shortcuts import get_object_or_404
from schedule.models import Calendar
school_classes_choices = ['Class Montessori','Class Nursery','Class LKG','Class UKG','Class One','Class Two','Class Three','Class Four','Class Five',
                          'Class Six','Class Seven','Class Eight','Class Nine','Class Ten']
semester_choices = ['First Semester','Second Semester','Third Semester','Fourth Semester','Fifth Semester','Sixth Semester','Seventh Semester','EIght Semester']
year_choices = ['First Year','Second Year','Third Year','Fourth Year','Fifth Year']
# semester_choices = (
#         ('First Semester ','First Semester'),
#         ('Second Semester','Second Semester'),
#         ('Third Semester','Third Semester'),
#         ('Fourth Semester','Fourth Semester'),
#         ('Fifth Semester','Fifth Semester'),
#         ('Sixth Semester','Sixth Semester'),
#         ('Seventh Semester','Seventh Semester'),
#         ('Eight Semester','Eight Semester'),
#     )

# year_choices = (
#         ('First Year','First Year'),
#         ('Second Year','Second Year'),
#         ('Third Year','Third Year'),
#         ('Fourth Year','Fourth Year'),
#         ('Fifth Year','Fifth Year'),
#     )
       
def populate_models(sender, **kwargs):
    a_level_admin, created = Group.objects.get_or_create(name='Admin')#a level admin
 
    bachelor_admin_group, created = Group.objects.get_or_create(name='Bachelor-Admin')
    master_admin_group, created = Group.objects.get_or_create(name='Master-Admin')
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    student_group, created = Group.objects.get_or_create(name='Student')
    parent_group, created = Group.objects.get_or_create(name='Parent')
    procurement_group, created = Group.objects.get_or_create(name='Procurement')
    finance_group, created = Group.objects.get_or_create(name='Finance')
    school_level, created = CourseCategory.objects.get_or_create(course_name="School")
    plus_two_level, created = CourseCategory.objects.get_or_create(course_name="Plus-Two")
    a_level, created = CourseCategory.objects.get_or_create(course_name="A-Level")
    diploma_level, created = CourseCategory.objects.get_or_create(course_name="Diploma")
    
    bachelor, created = CourseCategory.objects.get_or_create(course_name="Bachelor")
    master, created = CourseCategory.objects.get_or_create(course_name="Master")
    super_admin_group, created = Group.objects.get_or_create(name='Super-Admin')
    setting_object, created = MisSetting.objects.get_or_create(version='1.0')
    calendar_slug, created = Calendar.objects.get_or_create(name='event')
    if SemesterModel.objects.count()>0:
        pass
    else:
        SemesterModel.objects.bulk_create([
            # Using list comprehension to create SemesterModel objects
            SemesterModel(
                name = semester
            )
            for semester in semester_choices
        ])
    if YearModel.objects.count()>0:
        pass
    else:
        YearModel.objects.bulk_create([
            YearModel(
                name = year
            )
            for year in year_choices
        ])

    if Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'School')).exists():
        pass
    else:
        Semester.objects.bulk_create(
                                        [
                                            Semester(
                                                course_category = get_object_or_404(CourseCategory,course_name = "School"), 
                                                name=school_class
                                           ) 
                                            for school_class in school_classes_choices]
                                 )
    return [a_level_admin, bachelor_admin_group, master_admin_group,teacher_group,student_group,parent_group,super_admin_group ]
    
    


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    # extra_user_role = instance.user_type
    # try:
    #     # print(kwargs.get('role'),"role")
    #     print()
    #     print(Group.objects.get(pk=instance.user_type_id))
    #     print("in try","~~~~~~~~~~~~~~~~~~")
    # except:
    #     print("miss")
    if created:
        group = populate_models(sender)
        if instance.user_type in [group[0],group[1],group[2], group[6]]:
            AdminUser.objects.create(admin_user=instance)
        elif instance.user_type == group[3]:
            Staff.objects.create(staff_user=instance)
        elif instance.user_type == group[4]:
            Student.objects.create(student_user=instance)
        elif instance.user_type == group[5]:
            Parent.objects.create(parent_user=instance)
        else:
            ExtraUser.objects.create(extra_user=instance)
    

@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # extra_user_role = instance.user_type
    group = populate_models(sender)
    if instance.user_type in [group[0],group[1],group[2]]:
        instance.adminuser.save()
    if instance.user_type == group[3]:
        instance.staff.save()
    if instance.user_type == group[4]:
        instance.student.save()
    if instance.user_type == group[5]:
        instance.parent.save()
    # if instance.user_type == extra_user_role:
    #     instance.extrauser.save()









