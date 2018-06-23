# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Subject, UaFeature, Post

# Register your models here.

admin.site.register(Subject)
admin.site.register(UaFeature)
admin.site.register(Post)
