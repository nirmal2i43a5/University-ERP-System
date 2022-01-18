
"""it receives signal from ready function use in apps.py"""

from student_management_app.models import CustomUser,AdminUser,Staff,Student,Parent,ExtraUser,CourseCategory
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from school_apps.school_settings.models import MisSetting






def populate_models(sender, **kwargs):
    a_level_admin, created = Group.objects.get_or_create(name='Admin')
    bachelor_admin_group, created = Group.objects.get_or_create(name='Bachelor-Admin')
    master_admin_group, created = Group.objects.get_or_create(name='Master-Admin')
    teacher_group, created = Group.objects.get_or_create(name='Teacher')
    student_group, created = Group.objects.get_or_create(name='Student')
    parent_group, created = Group.objects.get_or_create(name='Parent')
    procurement_group, created = Group.objects.get_or_create(name='Procurement')
    finance_group, created = Group.objects.get_or_create(name='Finance')
    a_level, created = CourseCategory.objects.get_or_create(course_name="A-Level")
    bachelor, created = CourseCategory.objects.get_or_create(course_name="Bachelor")
    master, created = CourseCategory.objects.get_or_create(course_name="Master")
    super_admin_group, created = Group.objects.get_or_create(name='Super-Admin')
    setting_object, created = MisSetting.objects.get_or_create(version='1.0')
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









