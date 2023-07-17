from django.utils.text import slugify

import random
import string


def random_string_generator(size):
    return "".join(
        random.choices(
            string.ascii_lowercase +
            string.digits,
            k=size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.name)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug, randstr=random_string_generator(size=5)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
