from __future__ import unicode_literals

from django.db import models


class LiftPart(models.Model):
    name = models.CharField(max_length=255)
    vendor_code = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=4096, null=True, blank=True)
    full_description = models.TextField(max_length=4096, null=True, blank=True)
    image = models.ImageField()

    def __unicode__(self):
        return self.name
