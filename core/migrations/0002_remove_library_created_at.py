# Generated by Django 4.1.6 on 2023-02-10 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='library',
            name='created_at',
        ),
    ]
