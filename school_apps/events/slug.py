from django.utils.text import slugify

import random
import string

def random_string_generator(size):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=size)) 

def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.event_day[0:4])#slug generation for first four char in nepali date
    # ---------------------Below comment make slug unique with random str but i don't us this for now ------------------
    # Klass = instance.__class__
    # qs_exists = Klass.objects.filter(year=slug).exists()
    # if qs_exists:
    #     print("exists-----------")
    #     new_slug = "{slug}-{randstr}".format(
    #                 slug=slug,
    #                 randstr=random_string_generator(size=5)
    #             )
    #     return unique_slug_generator(instance, new_slug=new_slug)
    
    return slug