# Generated by Django 3.0.9 on 2020-10-13 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('references', '0005_ecosphere_industry'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ecosphere',
            name='industry',
        ),
        migrations.AddField(
            model_name='ecosphere',
            name='code',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='industry',
            name='code',
            field=models.CharField(max_length=5, null=True),
        ),
    ]
