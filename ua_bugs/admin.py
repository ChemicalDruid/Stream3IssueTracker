# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BugSubject, UaBug, BugPost

# Register your models here.
admin.site.register(BugSubject)
admin.site.register(UaBug)
admin.site.register(BugPost)
