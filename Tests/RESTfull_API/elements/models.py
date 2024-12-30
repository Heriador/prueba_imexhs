from django.db import models

from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Device(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=50,
        verbose_name='ID',
        blank=False
    )

    device_name = models.CharField(
        max_length=50,
        verbose_name='Device Name',
        blank=False
    )

    data = ArrayField(
        models.IntegerField(),
        verbose_name='Data',
        blank=False
    )

class Element(models.Model):
  
    device = models.OneToOneField(
        Device,
        on_delete=models.CASCADE,
        related_name='source_device',
    )
    average_before_normalization = models.FloatField(
        verbose_name='Average Before Normalization',
        blank=False
    )
    average_after_normalization = models.FloatField(
        verbose_name='Average After Normalization',
        blank=False
    )

    data_size = models.IntegerField(
        verbose_name='Data Size',
        blank=False
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created Date'
    )

    updated_date = models.DateTimeField(
        auto_now=True,
        verbose_name='Updated Date'
    )