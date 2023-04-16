from django.db import models
from datetime import date
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from setuptools.sandbox import save_argv, save_modules
from school_apps.events.slug import unique_slug_generator
from simple_history.models import HistoricalRecords
from .utils.DateConverter import _bs_to_ad
from .utils.utilities import get_nepali_digit
from datetime import datetime


class Event(models.Model):
    choices = (('Holiday','Holiday'),
               ('Event','Event'))
    
    title = models.CharField(max_length=200)
    event_day = models.CharField(_('Event Date'),max_length = 20)#default=date.today()
    english_date = models.DateField(null=True,blank=True)
    # year = models.SlugField(max_length=50, null=True,blank=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    description = models.TextField(null = True,blank= True)
    category = models.CharField(max_length=20, choices = choices)
    
    
    def __str__(self):
        return self.title
    
    def save(self,*args, **kwargs):
        nepali_day = self.event_day
        print(nepali_day)
        nep_date = nepali_day.split('-')
        '''Changing nepali char to english and passing it'''
        english_year_digit,english_month_digit,english_day_digit = get_nepali_digit(nep_date[0],nep_date[1],nep_date[2])
        year,month,day = _bs_to_ad(english_year_digit,english_month_digit,english_day_digit)
        eng = f'{year}-{month}-{day}'
        eng_date = ''.join(eng)
        parse_date = datetime.strptime(eng_date,'%Y-%m-%d').date()
        self.english_date = parse_date
        return super().save(*args, **kwargs)  


#I am slicing first four char of date and making it as slug
# @receiver(pre_save, sender=Event)
# def pre_save_receiver_event(sender, instance, *args, **kwargs):
    
#     if not instance.year:
#         instance.year = unique_slug_generator(instance)


