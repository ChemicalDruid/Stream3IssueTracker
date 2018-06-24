# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 21:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', tinymce.models.HTMLField(blank=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', tinymce.models.HTMLField()),
            ],
        ),
        migrations.CreateModel(
            name='UaBug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('bug_votes', models.IntegerField(default=0)),
                ('current_status', models.CharField(choices=[('tofix', 'tofix'), ('fixing', 'fixing'), ('fixed', 'fixed')], default='tofix', max_length=5)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bugs', to='ua_bugs.Subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bugs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='ua_bugs.UaBug')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='bug',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='ua_bugs.UaBug'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
    ]