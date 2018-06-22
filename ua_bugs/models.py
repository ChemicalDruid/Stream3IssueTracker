# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings
from django.utils import timezone


# Create your models here.
class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name


class UaBug(models.Model):
    status = (
        ('tofix', 'tofix'),
        ('fixing', 'fixing'),
        ('fixed', 'fixed'),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='bugs')
    subject = models.ForeignKey(Subject, related_name='bugs')
    created_at = models.DateTimeField(default=timezone.now)
    bug_votes = models.IntegerField(default=0)
    current_status = models.CharField(max_length=5, choices=status, default='tofix')


class Post(models.Model):
    bug = models.ForeignKey(UaBug, related_name='posts')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)


class Vote(models.Model):
    bug = models.ForeignKey(UaBug, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='votes')
