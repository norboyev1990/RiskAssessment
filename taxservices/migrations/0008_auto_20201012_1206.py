# Generated by Django 3.0.9 on 2020-10-12 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taxservices', '0007_auto_20201012_1158'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancesheet',
            name='balance_sect',
        ),
        migrations.RemoveField(
            model_name='balancesheet',
            name='balance_type',
        ),
        migrations.RemoveField(
            model_name='balancesheet',
            name='sect_name_ru',
        ),
        migrations.RemoveField(
            model_name='balancesheet',
            name='sect_name_uz',
        ),
        migrations.AddField(
            model_name='balancesheet',
            name='parentid',
            field=models.IntegerField(null=True),
        ),
    ]
