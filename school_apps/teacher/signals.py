# from school_apps.courses.models import *
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# @receiver(post_save, sender=studentgrades)
# def changerank(sender, instance, created, **kwargs):
#     rank = studentgrades.objects.filter(marks__gt=instance.marks).count()

#     grades = studentgrades.objects.filter(marks__lt=instance.marks)
#     for item in grades:
#         item.rank+= 1