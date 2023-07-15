
"""It receives signal from ready function use in apps.py"""

from student_management_app.models import CustomUser,AdminUser,Staff,Student,Parent,ExtraUser,CourseCategory,Semester,Subject
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from school_apps.school_settings.models import MisSetting
from django.shortcuts import get_object_or_404
from schedule.models import Calendar

# school_classes_choices = [
#                         'Class Montessori',
#                           'Class Nursery',
#                           'Class LKG',
#                           'Class UKG',
#                           'Class One',
#                           'Class Two',
#                           'Class Three',
#                           'Class Four',
#                           'Class Five',
#                           'Class Six',
#                           'Class Seven',
#                           'Class Eight',
#                           'Class Nine',
#                           'Class Ten'
#                           ]
# subjects_choices = [    'Nepali',    'English',    'Mathematics',    'Science',    'Social Studies', 'Computer Science' , 'Health,Population,& Environment', 
#                       'Moral Education',   'Creative Arts', ' Optional Mathematics',
#                         'Sanskrit (Optional)'
#                           ]

               
        
       
def populate_models(sender, **kwargs):
    a_level_admin, created = Group.objects.get_or_create(name='Admin')#a level admin
    bachelor_admin_group, created = Group.objects.get_or_create(name='Bachelor-Admin')
    master_admin_group, created = Group.objects.get_or_create(name='Master-Admin')
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    student_group, created = Group.objects.get_or_create(name='Student')
    parent_group, created = Group.objects.get_or_create(name='Parent')
    super_admin_group, created = Group.objects.get_or_create(name='Super-Admin')
    library_group, created = Group.objects.get_or_create(name='Library')

    # procurement_group, created = Group.objects.get_or_create(name='Procurement')
    # finance_group, created = Group.objects.get_or_create(name='Finance')
    school_level, created = CourseCategory.objects.get_or_create(course_name="School")
    plus_two_level, created = CourseCategory.objects.get_or_create(course_name="Plus-Two")
    a_level, created = CourseCategory.objects.get_or_create(course_name="A-Level")
    bachelor, created = CourseCategory.objects.get_or_create(course_name="Bachelor")
    master, created = CourseCategory.objects.get_or_create(course_name="Master")
    setting_object, created = MisSetting.objects.get_or_create(version='1.0')
    calendar_slug, created = Calendar.objects.get_or_create(name='event')
   
    # one_to_ten_class = Semester.objects.filter(course_category= CourseCategory.objects.get(course_name = 'School')).exclude(name__in=['Class Montessori',
    #                       'Class Nursery',
    #                       'Class LKG',
    #                       'Class UKG',])
  
        


    # '''Creating class from 1 to 10 directly'''
    # if Semester.objects.filter(course_category = get_object_or_404(CourseCategory, course_name = 'School')).exists():
    #     pass
    # else:
    #     Semester.objects.bulk_create(
    #                                     [
    #                                         Semester(
    #                                             course_category = get_object_or_404(CourseCategory,course_name = "School"), 
    #                                             name=school_class
    #                                        ) 
    #                                         for school_class in school_classes_choices]
    #                              )
    return [
            a_level_admin, 
            bachelor_admin_group, 
            master_admin_group,
            teacher_group,
            student_group,
            parent_group,
            super_admin_group,
            library_group
            ]
    
    

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
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
    group = populate_models(sender)
    if instance.user_type in [group[0],group[1],group[2]]:
        instance.adminuser.save()
    if instance.user_type == group[3]:
        instance.staff.save()
    if instance.user_type == group[4]:
        instance.student.save()
    if instance.user_type == group[5]:
        instance.parent.save()
    if instance.user_type == group[7]:
        instance.extrauser.save()
 
   









