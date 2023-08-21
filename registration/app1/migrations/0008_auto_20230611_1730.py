# Generated by Django 3.2.19 on 2023-06-11 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_attendence'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attendence',
            name='time',
        ),
        migrations.AddField(
            model_name='attendence',
            name='cnt',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='attendence',
            name='ftime',
            field=models.TimeField(null=True),
        ),
        migrations.AddField(
            model_name='attendence',
            name='status',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='attendence',
            name='stime',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='attendence',
            name='date',
            field=models.DateField(null=True),
        ),
    ]