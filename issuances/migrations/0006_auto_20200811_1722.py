# Generated by Django 3.0.9 on 2020-08-11 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issuances', '0005_auto_20200811_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='DATE_PERVOY_VYBOR',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='DATE_POGASH',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='DATE_VIDACHI',
            field=models.DateField(blank=True, null=True),
        ),
    ]
