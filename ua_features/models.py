# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

import uuid
from django.utils import timezone
from tinymce.models import HTMLField
from django.conf import settings
from paypal.standard.forms import PayPalPaymentsForm


# Create your models here.

class Subject(models.Model):
    name = models.CharField(max_length=255)
    description = HTMLField()

    def __unicode__(self):
        return self.name


class UaFeature(models.Model):
    status = (
        ('toadd', 'toadd'),
        ('adding', 'adding'),
        ('added', 'added'),
    )
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='features')
    subject = models.ForeignKey(Subject, related_name='features')
    created_at = models.DateTimeField(default=timezone.now)
    feature_votes_count = models.IntegerField(default=0)
    current_status = models.CharField(max_length=5, choices=status, default='toadd')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=5.00)

    @property
    def paypal_form(self):
        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": self.price,
            "currency": "EUR",
            "item_name": self.name,
            "invoice": "%s-%s" % (self.pk, uuid.uuid4()),
            "notify_url": settings.PAYPAL_NOTIFY_URL,
            "return_url": "%s/paypal-return" % settings.SITE_URL,
            "cancel_return": "%s/paypal-cancel" % settings.SITE_URL
        }

        return PayPalPaymentsForm(initial=paypal_dict)

    def __unicode__(self):
        return self.name


class Post(models.Model):
    feature = models.ForeignKey(UaFeature, related_name='feature_posts')
    comment = HTMLField(blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feature_posts')
    created_at = models.DateTimeField(default=timezone.now)


class Vote(models.Model):
    feature = models.ForeignKey(UaFeature, related_name='feature_votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='feature_votes')
