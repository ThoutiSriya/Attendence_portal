# Generated by Django 3.2.9 on 2023-06-04 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stu',
            name='type',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
