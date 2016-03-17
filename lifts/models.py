# coding=utf-8
from __future__ import unicode_literals

from django.db import models


class LiftPart(models.Model):
    LIFTPARTS=1
    LIFTBOARD=2
    LIFTOTIS=3
    KINDS=(
        (LIFTPARTS,"ЛИФТОВЫЕ ЗАПЧАСТИ"),
        (LIFTBOARD,"ЛИФТОВЫЕ ПЛАТЫ"),
        (LIFTOTIS,"OTIS ЗАПЧАСТИ")
    )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=4096, null=True, blank=True)
    full_description = models.TextField(max_length=4096, null=True, blank=True)
    image = models.ImageField()
    kind=models.IntegerField(null=True,choices=KINDS)

    def __unicode__(self):
        return self.name
