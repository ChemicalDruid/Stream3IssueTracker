# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Subject, UaBug, Post


# Register your models here.
admin.site.register(Subject)
admin.site.register(UaBug)
admin.site.register(Post)
