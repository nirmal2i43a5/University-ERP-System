from django import template
from datetime import datetime, timedelta

register = template.Library()


@register.filter
def days_until_expiry(expiry_date):
    return (expiry_date - datetime.today().date()).days
