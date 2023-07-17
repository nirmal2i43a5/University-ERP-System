from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models


class Transport(models.Model):
    route_name = models.CharField(max_length=100)
    route_fare = models.DecimalField(max_digits=10, decimal_places=2)
    no_of_vehicle = models.PositiveIntegerField()
    driver_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tbl_Transport"
        verbose_name = _("transport")
        verbose_name_plural = _("transports")

    def __str__(self):
        return self.route_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
