# Generated by Django 3.2.9 on 2023-06-05 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_fac'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stu',
            old_name='type',
            new_name='ids',
        ),
        migrations.RemoveField(
            model_name='fac',
            name='type',
        ),
    ]
