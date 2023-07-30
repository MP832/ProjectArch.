from django.db import models
from django.contrib.auth.models import User,Group
import os

User._meta.get_field('email')._unique = False


class Bezoeker(models.Model):
    fname = models.CharField(max_length=55,blank=False)
    lname = models.CharField(max_length=55,blank=False)
    functie = models.CharField(blank=False, max_length=55)
    email = models.CharField(blank=False, max_length=70, default='MP')
    evenements = models.CharField(blank=False, max_length=55, default='MP')
    aanwezigheid = models.IntegerField(blank=False)

    def __str__(self):
        return self.email


class evenement(models.Model):
    name = models.CharField(max_length=55, blank=False)
    maillijst = models.FileField(upload_to="uploads/")
    onderwerpmail = models.CharField(max_length=70, blank=False)
    mailtemplate = models.TextField()
    mailtemplateoutlook = models.TextField()

    def __str__(self):
        return self.name