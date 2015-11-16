# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('number', models.PositiveIntegerField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('is_new_testament', models.BooleanField()),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(db_index=True)),
                ('book', models.ForeignKey(related_name='chapters', to='bible.Book')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Verse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(db_index=True)),
                ('text', models.TextField()),
                ('chapter', models.ForeignKey(related_name='verses', to='bible.Chapter')),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='verse',
            unique_together=set([('chapter', 'number')]),
        ),
        migrations.AlterUniqueTogether(
            name='chapter',
            unique_together=set([('book', 'number')]),
        ),
    ]
